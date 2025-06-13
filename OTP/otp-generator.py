import sys
import hmac, base64, struct, hashlib, time
import cryptography

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

    @staticmethod
    def get_hotp_token(secret, intervals_no):
        try:
            key = base64.b32decode(secret, True) #* DECODING KEY IN BASE 32
        except base64.binascii.Error:
            raise ValueError("Invalid Base32 secret: Ensure the secret is properly Base32-encoded.")
        
        msg = struct.pack(">Q", intervals_no) #* CONVERT PYTHON VAL IN C STRUCT
        
        h = hmac.new(key, msg, hashlib.sha1).digest() #* GENERATE HASH WITH KEY AND MSG
        o = o = h[19] & 15
        
        h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000 #UNPACKING
            
        return h
    
    def get_totp_token(self, secret):
        x = str(self.get_hotp_token(secret, intervals_no=int(time.time())//30)) # CHECK IF OTP IS SAME FOR 30s
        
        while(len(x) != 6):
            x+='0'
        return x

    def process(self):
        
        print("\033[1;35mPlease enter the encryption key for the file:\033[0m")
        encryption_key = scanf("%s")

        try:
            encryption_key = encryption_key[0].encode()
            fernet = Fernet(encryption_key)
            try:
                with open(self.enc_file_path, 'rb') as enc_file:
                    encrypted = enc_file.read()
                self.key = fernet.decrypt(encrypted)
            except cryptography.fernet.InvalidToken:
                print("\033[91mError: Invalid encryption key. Decryption failed.\033[0m")
                sys.exit()
        except Exception as e:
            print(f"\033[91mError: Invalid encryption key. \033[0m")
            sys.exit()
        
        with open(self.enc_file_path, 'rb') as enc_file:
            encrypted = enc_file.read()
            
        self.key = fernet.decrypt(encrypted)
        
        print("\n\033[1;32mThe encryption key is valid and the file has been successfully decrypted.\033[0m\n\n")
        
        try:
            while True:
                try:
                    decoded_key = base64.b32encode(self.key).decode('utf-8')
                    print("\033[F\033[K", end='')
                    print(f"\t\033[1;33m🔑 {self.get_totp_token(decoded_key)}\033[0m")
                    time.sleep(1)  # Wait for 1 second before generating the next token
                except Exception as e:
                    print(f"\033[91mError: Failed to Base32-encode the key. {e}\033[0m")
                    sys.exit()
        except KeyboardInterrupt:
            print("\n\033[91mProcess interrupted by user. Bye bye...\033[0m")
            sys.exit()
        

        
        
        
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
