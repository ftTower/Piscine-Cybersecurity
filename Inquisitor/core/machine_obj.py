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


# def thread_function(obj):
#     # log_info(f"thread {obj.type} started")
    
#     interface = "enp0s3"
#     # cap = None
#     # log_info(f"Thread '{obj.type}' for ARP monitoring started on interface: {interface}")
    
#     try :
#         obj.cap_handle = pcapy.open_live(interface, 65535, True, 100)
#         obj.cap_handle.setfilter("arp")
        
#         def poisoning_setter(header,data):
#             sender_mac, sender_ip, target_mac, target_ip = process_packet(header, data, obj)
#             if sender_mac and target_mac:
#                 #! PUT ARP REPLY
#                 obj.poisoned = True
#                 log_success(f"{obj}")

#         while not threading_end_event.is_set():
#             if not obj.poisoned:
#                 packets_received = obj.cap_handle.dispatch(1, poisoning_setter)
                
#                 if packets_received == 0 and not threading_end_event.is_set():
#                     threading_end_event.wait(0.05)
#             else:
#                 #! PUT ARP REPLY TO MAINTAIN SPOOFING
#                 threading_end_event.wait(2)
#                 pass
                
#     except pcapy.PcapError as e:
#         log_error(f"Pcapy error during capture on '{interface}': {e}")
#         log_error("Ensure the script runs with root privileges (sudo).")
#         log_error(f"Verify that interface '{interface}' exists and is operational.")
#     except Exception as e:
#         log_error(f"An unexpected error occurred in ARP capture thread: {e}")
#     finally:
#         if obj.cap_handle:
#             obj.cap_handle.close()

#     # log_info(f"thread {obj.type} stoped")

class Machine:
    def __init__(self, mac_address, ip_address, type, mac_attacker=None):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.mac_attacker = mac_attacker
        
        self.type = type
        self.poisoned = False
        self.cap_handle = None
    
        #? FOR ATTACKER MACHINE
        if mac_address == None:
           self.find_mac_adress() 
    
        #? FOR ALL MACHINES VERIFY DATA FORMAT
        self.verify_ip_adress()
        self.verify_mac_adress()
        
        log_debug(self)

        # #? WE WANT TO CHECK FOR BOTH TARGET REQUESTS AND POISON THEM
        # if self.type == "Source" or self.type == "Target":
        #     thread = threading.Thread(target=thread_function, args=(self,), name=f"Machine-{type}-Thread", daemon=False)
        #     thread.start()
    
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
    