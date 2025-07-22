from machine_obj import *
from ainsi import *

import sys
from datetime import datetime

def get_output_file_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

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