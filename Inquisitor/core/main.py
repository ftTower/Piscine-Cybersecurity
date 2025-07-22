import sys
from inquisitor_obj import *
from ainsi import *

def safe_exit(inquisitor):
	threading_end_event.set()
	print(f"\n{erase_lines(2)}", end="")
 
	for thread in threading.enumerate():
		if thread is not threading.main_thread():
			thread.join(timeout=5)
			if thread.is_alive():
				log_error(f"Thread {thread.name} did not terminate gracefully.")
		log_success(f"Thread {colored(thread.name, YELLOW)} terminate.")
	log_success("ARP monitor stopped.")
	sys.exit(0)

def main():
	if len(sys.argv) != 5:
		sys.exit(1)

	try:
		
		inquisitor = Inquisitor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

		# while not threading_end_event.is_set():
		# 	threading_end_event.wait(0.5)
		inquisitor.looking_for_arp_requests()

	except KeyboardInterrupt:
		safe_exit(inquisitor)
	except Exception as e:
		log_error(f"Fail in main loop :\t{e}")

	return 0

if __name__ == "__main__":
    print()
    log_info("Starting ARP monitor...\n")	
    main()
    print()
