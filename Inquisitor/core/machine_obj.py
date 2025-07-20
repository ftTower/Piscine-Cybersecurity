

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

