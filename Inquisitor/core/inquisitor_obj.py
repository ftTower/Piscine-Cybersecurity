from machine_obj import *
from ainsi import *

import sys
from datetime import datetime
import struct
import socket
import pcapy
import threading

ETH_HLEN = 14
ARP_ETHERTYPE = 0x0806 #! ARP TYPE
ARP_REQUEST_OP = 1
ARP_REPLY_OP = 2

def get_output_file_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def process_packet(header, data):
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

            print(f"  Expéditeur MAC : {sender_mac}")
            print(f"  Expéditeur IP  : {sender_ip}")
            print(f"  Cible MAC      : {target_mac}")
            print(f"  Cible IP       : {target_ip}")

    except struct.error as e:
        log_error(f"Packet decoding error (struct.error): {e}")
    except IndexError as e:
        log_error(f"Index error (packet too short or malformed): {e}")
    except Exception as e:
        log_error(f"An unexpected error occurred while processing the packet: {e}")
    return sender_mac, sender_ip, target_mac, target_ip

class Inquisitor:
    def __init__(self, source_ip, source_mac, target_ip, target_mac):
        self.source = Machine(source_mac, source_ip, "Source")
        self.target = Machine(target_mac, target_ip, "Target")
        self.attacker = Machine(None, None, "attacker")

        self.ouput_file = get_output_file_name()
        
    #! MAN IN THE MIDDLE

    def looking_for_arp_requests(self):
        # interface = "enp0s3"
        
        # log_info(f"Démarrage de l'écoute des requêtes ARP sur l'interface : {interface}")

        # try : 
        #     cap = pcapy.open_live(interface, 65535, True, 0)
        #     cap.setfilter("arp")
        #     log_info("Écoute active des requêtes ARP (Appuyez sur CTRL+C pour arrêter)...")
        #     cap.loop(-1, process_packet)

        # except pcapy.PcapError as e:
        #     log_error(f"Erreur Pcapy lors de la capture : {e}")
        #     log_error("Assurez-vous d'exécuter le script avec des privilèges root (sudo).")
        #     log_error(f"Vérifiez que l'interface '{interface}' existe et est opérationnelle.")
        # except KeyboardInterrupt:
        #     log_info("\nArrêt de l'écoute des requêtes ARP demandé par l'utilisateur.")
        #     # Ici, vous pourriez ajouter du code pour restaurer les tables ARP si l'attaque était active.
        #     # Pour l'écoute simple, il n'y a rien à restaurer.
        # except Exception as e:
        #     log_error(f"Une erreur inattendue s'est produite dans la fonction looking_for_arp_requests: {e}")
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