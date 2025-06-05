import sys
from cryptography.fernet import Fernet
from scanf import scanf

#! CLASSES

class hexa_process:
    def __init__(self, file_path, file):
        self.file_path = file_path
        self.fichier   = file
        
        self.hexakey   = file.read()
        
        self.key = Fernet.generate_key()
        
    def __str__(self):
        return self.hexakey
    
    @staticmethod
    def check_hexakey(hexakey):
        try:
            int(hexakey, 16)
        except ValueError:
            raise ValueError("Invalid hex key: The provided key is not a valid hexadecimal value.")
        
    def process(self):
        
        self.check_hexakey(self.hexakey)  #*CHECKING IF KEY IS HEXA         
        
        # print(self.hexakey)
            
        print(f"\n\033[1;91mENCRYPTION KEY GENERATED: \033[1;93m{self.key.decode()}\033[0m")
        print("\033[1;91mSTORE IT SECURELY!\033[0m\n")
        
        fernet = Fernet(self.key)
        
        with open(self.file_path, 'rb') as file:
            original = file.read()
            
        encrypted = fernet.encrypt(original)
        
        with open('ft_otp.key', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        
#!---------------------------------------------------------------------------------------------#!
        
class string_process:
    def __init__(self, enc_file_path):
        self.enc_file_path = enc_file_path
        self.key = None

    def process(self):
        
        print("\033[1;35mPlease enter the encryption key for the file:\033[0m")
        encryption_key = scanf("%s")

        try:
            encryption_key = encryption_key[0].encode()
            fernet = Fernet(encryption_key)
        except Exception as e:
            print(f"\033[91mError: Invalid encryption key. {e}\033[0m")
            sys.exit()
        
        with open(self.enc_file_path, 'rb') as enc_file:
            encrypted = enc_file.read()
            
        self.key = fernet.decrypt(encrypted)
        
        print("\033[1;32mThe encryption key is valid and the file has been successfully decrypted.\033[0m")
        print(f"\n{self.key.decode()}")
        
        
        
#! FUNCTIONS        
        
def check_args(argv):
    if (len(sys.argv) < 3 or len(sys.argv) > 3):
        print("\033[91mError: Usage: python3 otp-generator.py <-g key.hex> <-k keystring>\033[0m")
        sys.exit()
    elif "-g" in sys.argv:
        g_index = sys.argv.index("-g")
        if g_index + 1 < len(sys.argv):
            print(f"\033[94mEncrypting your 64 hexa password in {sys.argv[g_index + 1]}\033[0m")
            return sys.argv[g_index + 1]
        else :
            print("\033[91mError: Missing argument for -g. Usage: python3 otp-generator.py -g <key.hex>\033[0m")
            sys.exit()
    elif "-k" in sys.argv:
        k_index = sys.argv.index("-k")
        if k_index + 1 < len(sys.argv):
            print(f"\033[94mDecrypting your 64 hexa password in {sys.argv[k_index + 1]}\033[0m\n")
            return sys.argv[k_index + 1]
        else :
            print("\033[91mError: Missing argument for -k. Usage: python3 otp-generator.py -k <string_key>\033[0m")
            sys.exit()
    else:
        sys.exit()
    
def define_process(parameter):
    if parameter.endswith(".hex"):
        try :
            file = open(parameter.strip(), "r")
            process_instance = hexa_process(parameter.strip(), file)
            process_instance.process()
            file.close()

        except Exception as e:
            print(f"Error: {e}")
            sys.exit()
    else:
        string_process(parameter).process()
        
        
        
#! PROCESS

define_process(check_args(sys.argv))
