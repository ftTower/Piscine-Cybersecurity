from machine_obj import *

import sys
from datetime import datetime


def get_output_file_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"


class Inquisitor:
    def __init__(self, source_mac, source_ip, target_mac, target_ip):
        self.source = Machine(source_mac, source_ip, "Source")
        self.target = Machine(target_mac, target_ip, "Target")
        self.attacker = Machine(None, None, "attacker")

        self.ouput_file = get_output_file_name()



    def looking_for_arp_requests(self):
        pass
    
    def poisoned_arp_reply(self, ip_address):
        pass
    
    def capturing_packets(self):
        pass
    
    def save_packets(self):
        pass