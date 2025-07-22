from ainsi import *

from getmac import get_mac_address as gma
import ipaddress
import re
import pcapy
import struct
import socket

import threading
import time


ETH_HLEN = 14
ARP_ETHERTYPE = 0x0806 #! ARP TYPE
ARP_REQUEST_OP = 1
ARP_REPLY_OP = 2

threading_end_event = threading.Event()


def process_packet(header, data, machine):
    sender_mac, sender_ip, target_mac, target_ip = None, None, None, None
    try:
        eth_type = struct.unpack("!H", data[12:14])[0]

        if eth_type == ARP_ETHERTYPE:
            arp_packet = data[ETH_HLEN:]

            operation = struct.unpack("!H", arp_packet[6:8])[0]

            if operation == ARP_REQUEST_OP:
                log_info(f"Found an arp request")

            sender_mac_bytes = arp_packet[8:14]
            sender_mac = ":".join(f"{b:02x}" for b in sender_mac_bytes)

            sender_ip_bytes = arp_packet[14:18]
            sender_ip = socket.inet_ntoa(sender_ip_bytes)

            target_mac_bytes = arp_packet[18:24]
            target_mac = ":".join(f"{b:02x}" for b in target_mac_bytes)

            target_ip_bytes = arp_packet[24:28]
            target_ip = socket.inet_ntoa(target_ip_bytes)

            # print(f"  Expéditeur MAC : {sender_mac}")
            # print(f"  Expéditeur IP  : {sender_ip}")
            # print(f"  Cible MAC      : {target_mac}")
            # print(f"  Cible IP       : {target_ip}")

        if sender_ip != machine.ip_address or sender_mac != machine.mac_address:
            return None, None, None, None

    except struct.error as e:
        log_error(f"Packet decoding error (struct.error): {e}")
    except IndexError as e:
        log_error(f"Index error (packet too short or malformed): {e}")
    except Exception as e:
        log_error(f"An unexpected error occurred while processing the packet: {e}")
    return sender_mac, sender_ip, target_mac, target_ip


def thread_function(obj):
    # log_info(f"thread {obj.type} started")
    
    interface = "enp0s3"
    cap = None
    log_info(f"Thread '{obj.type}' for ARP monitoring started on interface: {interface}")
    
    try :
        cap = pcapy.open_live(interface, 65535, True, 100)
        cap.setfilter("arp")
        
        def poisoning_setter(header,data):
            sender_mac, sender_ip, target_mac, target_ip = process_packet(header, data, obj)
            if sender_mac and target_mac:
                obj.poisoned = True
                log_success(f"{obj}")

        while not threading_end_event.is_set():
            if not obj.poisoned:
                packets_received = cap.dispatch(-1, poisoning_setter)
                
                if packets_received == 0:
                    threading_end_event.wait(0.01)
            else:
                #! PUT ARP REPLY
                pass
                
    except pcapy.PcapError as e:
        log_error(f"Pcapy error during capture on '{interface}': {e}")
        log_error("Ensure the script runs with root privileges (sudo).")
        log_error(f"Verify that interface '{interface}' exists and is operational.")
    except Exception as e:
        log_error(f"An unexpected error occurred in ARP capture thread: {e}")
    finally:
        if cap:
            cap.close()
            log_info(f"Pcapy capture on '{interface}' closed.")

    # log_info(f"thread {obj.type} stoped")


class Machine:
    def __init__(self, mac_address, ip_address, type):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.type = type
        self.poisoned = False
    
    def __init__(self, mac_address, ip_address, type):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.type = type
        self.poisoned = False
    
        #? FOR ATTACKER MACHINE
        if mac_address == None:
           self.find_mac_adress() 
    
        #? FOR ALL MACHINES VERIFY DATA FORMAT
        self.verify_ip_adress()
        self.verify_mac_adress()
        
        log_debug(self)

        #? WE WANT TO CHECK FOR BOTH TARGET REQUESTS AND POISON THEM
        if self.type == "Source" or self.type == "Target":
            thread = threading.Thread(target=thread_function, args=(self,), name=f"Machine-{type}-Thread")
            thread.start()
    
    #! VERIFY INFORMATION GIVED
    def verify_ip_adress(self):
        if not self.ip_address:
            return 
        ipaddress.ip_address(self.ip_address) 
    
    def verify_mac_adress(self):
        if not self.ip_address:
            return
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_pattern.match(self.mac_address):
            raise Exception("Invalid MAC address format")
    
    #! FIND MAC ADRESS FOR ATTACKER
    def find_mac_adress(self):
        self.mac_address = gma()
    
    #! RESTORE ARP FOR ONE TARGET
    def restore_arp_table(self):
        pass
    
    #! UTILS
    
    def __str__(self):
        type_str = str(colored(self.type, BRIGHT_YELLOW)) if self.type is not None else "None"
        ip_str = str(self.ip_address) if self.ip_address is not None else "None"
        mac_str = str(self.mac_address) if self.mac_address is not None else "None"
        poisoned_str = str(self.poisoned)
        return f"{type_str:<17} | IP: {ip_str:<15} | MAC: {mac_str:<17} | Poisoned: {poisoned_str:<5}"
    