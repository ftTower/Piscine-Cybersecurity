import sys
from inquisitor_obj import *
from ainsi import *

def safe_exit():
	threading_end_event.set()
	print(f"\n{erase_lines(2)}", end="")
	for thread in threading.enumerate():
		if thread is not threading.main_thread():
			thread.join(timeout=10)
			if thread.is_alive():
				log_error(f"Thread {thread.name} did not terminate gracefully.")
		log_success(f"Thread {colored(thread.name, YELLOW)} terminate.")
	log_success("ARP monitor stopped.")

def main():
	if len(sys.argv) != 5:
		sys.exit(1)

	try:
		
		inquisitor = Inquisitor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

		# while True:
			# if not inquisitor.target.poisoned or not inquisitor.source.poisoned:
			# 	inquisitor.poisoned_arp_reply(inquisitor.looking_for_arp_requests())
			# else:
			# 	inquisitor.save_packets(inquisitor.capturing_packets())
			# continue
   
		while not threading_end_event.is_set():
			time.sleep(1)

	except KeyboardInterrupt:
		safe_exit()
	except Exception as e:
		log_error(f"Fail in main loop :\t{e}")

	return 0

if __name__ == "__main__":
    print()
    log_info("Starting ARP monitor...\n")	
    main()
    print()
