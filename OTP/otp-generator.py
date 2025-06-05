import sys

class hexa_process:
    def __init__(self, file_path):
        self.file_path = file_path

    def process(self):
        print("Processing hexa key")

class string_process:
    def __init__(self, key):
        self.key = key

    def process(self):
        print("Processing string key")


def check_args(argv):
    if (len(sys.argv) < 3 or len(sys.argv) > 3):
        print("\033[91mError: Usage: python3 otp-generator.py <-g key.hex> <-k keystring>\033[0m")
        sys.exit()
    elif "-g" in sys.argv:
        g_index = sys.argv.index("-g")
        if g_index + 1 < len(sys.argv):
            print(f"\033[94mProcessing -g option with argument: {sys.argv[g_index + 1]}\033[0m")
            return sys.argv[g_index + 1]
        else :
            print("\033[91mError: Missing argument for -g. Usage: python3 otp-generator.py -g <key.hex>\033[0m")
            sys.exit()
    elif "-k" in sys.argv:
        k_index = sys.argv.index("-k")
        if k_index + 1 < len(sys.argv):
            print(f"\033[94mProcessing -k option with argument: {sys.argv[k_index + 1]}\033[0m")
            return sys.argv[k_index + 1]
        else :
            print("\033[91mError: Missing argument for -k. Usage: python3 otp-generator.py -k <string_key>\033[0m")
            sys.exit()
    else:
        sys.exit()
    
def define_process(parameter):
    if parameter.endswith(".hex"):
        try :
            open(parameter.strip(), "r")
            hexa_process(parameter.strip()).process()
        except Exception as e:
            print("Error: Failed to open file")
            sys.exit()
    else:
        string_process(parameter).process()
        
        
#! PROCESS

define_process(check_args(sys.argv))




print("\033[92mGeneration complete!\033[0m")