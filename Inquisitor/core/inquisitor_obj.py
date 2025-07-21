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