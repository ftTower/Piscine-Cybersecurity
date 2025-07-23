from ainsi import *

ETH_HLEN = 14
ARP_ETHERTYPE = 0x0806 #! ARP TYPE
ARP_REQUEST_OP = 1
ARP_REPLY_OP = 2

import pcapy
import struct
import socket

import threading
import time

threading_end_event = threading.Event()

def process_packet(header, data, inquisitor):
    sender_mac, sender_ip, target_mac, target_ip = None, None, None, None
    try:
        eth_type = struct.unpack("!H", data[12:14])[0]

        if eth_type == ARP_ETHERTYPE:
            arp_packet = data[ETH_HLEN:]

            operation = struct.unpack("!H", arp_packet[6:8])[0]

            if operation == ARP_REQUEST_OP:
                #! HERE WE GET ALL WE NEED TO KNOW (IP/MAC of SENDER + TARGET)
                sender_mac_bytes = arp_packet[8:14]
                sender_mac = ":".join(f"{b:02x}" for b in sender_mac_bytes)

                sender_ip_bytes = arp_packet[14:18]
                sender_ip = socket.inet_ntoa(sender_ip_bytes)

                target_mac_bytes = arp_packet[18:24]
                target_mac = ":".join(f"{b:02x}" for b in target_mac_bytes)

                target_ip_bytes = arp_packet[24:28]
                target_ip = socket.inet_ntoa(target_ip_bytes)

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
