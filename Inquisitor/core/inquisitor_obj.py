from machine_obj import *
from ainsi import *

import sys
from datetime import datetime

def get_output_file_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def process_packet(header, data, inquisitor):
    sender_mac, sender_ip, target_mac, target_ip = None, None, None, None
    try:
        eth_type = struct.unpack("!H", data[12:14])[0]

        if eth_type == ARP_ETHERTYPE:
            arp_packet = data[ETH_HLEN:]

            operation = struct.unpack("!H", arp_packet[6:8])[0]

            if operation == ARP_REQUEST_OP:
                # log_info(f"Found an arp request")

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

    except struct.error as e:
        log_error(f"Packet decoding error (struct.error): {e}")
    except IndexError as e:
        log_error(f"Index error (packet too short or malformed): {e}")
    except Exception as e:
        log_error(f"An unexpected error occurred while processing the packet: {e}")

    if sender_ip == inquisitor.source.ip_address and target_ip == inquisitor.target.ip_address:
        return sender_mac, sender_ip, target_mac, target_ip
    elif target_ip == inquisitor.source.ip_address and sender_ip == inquisitor.target.ip_address:
        return sender_mac, sender_ip, target_mac, target_ip
    else:
        return None, None, None, None


class Inquisitor:
    def __init__(self, source_ip, source_mac, target_ip, target_mac):
        self.attacker = Machine(None, None, "attacker")
        self.source = Machine(source_mac, source_ip, "Source", mac_attacker=self.attacker.mac_address)
        self.target = Machine(target_mac, target_ip, "Target", mac_attacker=self.attacker.mac_address)

        self.ouput_file = get_output_file_name()
        
    #! MAN IN THE MIDDLE

    def looking_for_arp_requests(self):
        interface = "enp0s3"
        
        log_info(f"Démarrage de l'écoute des requêtes ARP sur l'interface : {interface}")

        try:
            cap = pcapy.open_live(interface, 65535, True, 100)
            cap.setfilter("arp")
            log_info("Écoute active des requêtes ARP (Appuyez sur CTRL+C pour arrêter)...")
            while True:
                header, packet = cap.next()
                if header is not None and packet is not None:
                   sender_mac, sender_ip, target_mac, target_ip = process_packet(header, packet, self)
                
                print(f"from {sender_ip} to {target_ip}")
                
                if sender_ip == self.source.ip_address:
                    self.source.poisoned = True
                elif sender_ip == self.target.ip_address:
                    self.target.poisoned = True
                    
                if self.source.poisoned and self.target.poisoned:
                    break
                  
        except KeyboardInterrupt:
            log_info("\nArrêt de l'écoute des requêtes ARP demandé par l'utilisateur.")
        except pcapy.PcapError as e:
            log_error(f"Erreur Pcapy lors de la capture : {e}")
            log_error("Assurez-vous d'exécuter le script avec des privilèges root (sudo).")
            log_error(f"Vérifiez que l'interface '{interface}' existe et est opérationnelle.")
        except Exception as e:
            log_error(f"Une erreur inattendue s'est produite dans la fonction looking_for_arp_requests: {e}")
        pass

    def poisoned_arp_reply(self, ip_address):
        if not ip_address:
            return 
        log_info(f"Poisoning {ip_address}...")
        pass
    
    def capturing_packets(self):
        pass
    
    def save_packets(self):
        pass