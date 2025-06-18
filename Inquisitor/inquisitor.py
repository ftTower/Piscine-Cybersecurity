import os
import sys
import socket

class machine:
    
    def __init__(self, IPv4, MacAdress):
        
        self.IPv4 = self.check_IPv4(IPv4)
        self.MacAdress = MacAdress
        
    def __str__(self):
        return self.IPv4 + " : " + self.MacAdress
    
    def check_IPv4(self, IPv4):
        try:
            socket.inet_pton(socket.AF_INET, IPv4)
        except AttributeError:
            try:
                socket.inet_aton(IPv4)
            except socket.error:
                raise ValueError(f"Invalid IPv4 address: {IPv4}")
            if IPv4.count('.') != 3:
                raise ValueError(f"Invalid IPv4 address: {IPv4}")
        except socket.error:
            raise ValueError(f"Invalid IPv4 address: {IPv4}")
        return IPv4
    
class inquisitor:
    def __init__(self, argv):
        
        #! INITING MACHINE
        try:
            self.src = machine(argv[1], argv[2])
            self.target = machine(argv[3], argv[4])
        except Exception as e:
            print(f"INITING ERROR : {e}")
        

if (len(sys.argv) == 5):
    inquisitor(sys.argv)
else: 
    print("python3 ./inquisitor <IP_src> <Mac_src> <IP_target> <Mac_target>")


# inquisitor(sys.argv)