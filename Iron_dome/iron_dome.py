import os
import sys
import psutil
import time

maximum_usage_to_alert = 90 #! in %
file_path_to_alert = "/var/log/irondome/irondome.log"

class iron_dome:
    def __init__(self, argv):
        self.paths = []
        self.check_paths(argv)
        self.run()        
        
        
    def check_paths(self, argv):
        for path in argv:
            if "./iron_dome.py" in path:
                continue
            elif os.path.isdir(path) is True: 
                self.paths.append(path)
            else:
                print(f"\033[31mCannot use this path; it is not a folder: {path}\033[0m")
    
    def disk_usage(self, path):
        disk_usage = psutil.disk_usage('/')
        print(f"{path}: \033[93m{disk_usage.percent}%\033[0m")
    
    def run(self):
        print("running..")
        while True: 
            
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"\nCPU Usage: \033[91m{cpu_usage}%\033[0m")
            
            memory = psutil.virtual_memory()
            print(f"Memory Usage: \033[92m{memory.percent}%\033[0m")
            
            print("Disk Usage : ")
            for path in self.paths:
                self.disk_usage(path)
            
            network = psutil.net_io_counters()
            print(f"Bytes Sent: \033[94m{network.bytes_sent}\033[0m, Bytes Received: \033[95m{network.bytes_recv}\033[0m")
            
            time.sleep(0.5)


            print("\033[F\033[K" * (len(self.paths) + 5), end="")
        
        

if (len(sys.argv) < 2):
    print("\n\033[31mpython3 ./iron_dome <folder_path_to_inspect_usage> <other folders..>\033[0m\n")
    exit(1)
    
iron_dome(sys.argv)
    
#! reste a faire lecriture dans le fichier 