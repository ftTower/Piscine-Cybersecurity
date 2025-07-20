import sys
from datetime import datetime

class Machine:
    def __init__(self, mac_address, ip_address, type):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.type = type
        self.poisoned = False
    
        if mac_address == None:
           self.find_mac_adress() 
    
        
    
    def __str__(self):
        return f"{self.type} : '{self.ip_address}' {self.mac_address} {self.poisoned}"
    
    def find_mac_adress(self):
        pass
    
    def restore_arp_table(self):
        pass




def get_output_file_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"


class Inquisitor:
    def __init__(self, target_mac, target_ip, source_mac, source_ip):
        self.target = Machine(target_mac, target_ip, "Target")
        self.source = Machine(source_mac, source_ip, "Source")
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