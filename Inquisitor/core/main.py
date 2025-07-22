import sys
from inquisitor_obj import *
from ainsi import *
def safe_exit(inquisitor):
    print("\n" + ERASE_LINE) # Added newline for cleaner output before erase
    log_success("ARP monitor stopping. Signalling threads to exit...")
    
    threading_end_event.set() # Signal all threads to stop their loops

    if inquisitor: 
        
        # --- Handle Source's cap_handle ---
        if hasattr(inquisitor.source, 'cap_handle') and inquisitor.source.cap_handle is not None:
            log_debug(f"Calling breakloop for Source thread's capture handle...")
            try:
                if isinstance(inquisitor.source.cap_handle, pcapy.Capture):
                    inquisitor.source.cap_handle.breakloop()
                else:
                    log_error(f"Source cap_handle is not a pcapy.Capture object: {type(inquisitor.source.cap_handle)}")
            except Exception as e:
                log_error(f"Error calling breakloop for Source: {e}")
        else:
            log_debug("Source cap_handle not initialized or found.")

        # --- Handle Target's cap_handle ---
        if hasattr(inquisitor.target, 'cap_handle') and inquisitor.target.cap_handle is not None:
            log_debug(f"Calling breakloop for Target thread's capture handle...")
            try:
                if isinstance(inquisitor.target.cap_handle, pcapy.Capture):
                    inquisitor.target.cap_handle.breakloop()
                else:
                    log_error(f"Target cap_handle is not a pcapy.Capture object: {type(inquisitor.target.cap_handle)}")
            except Exception as e:
                log_error(f"Error calling breakloop for Target: {e}")
        else:
            log_debug("Target cap_handle not initialized or found.")

        # --- Join threads ---
        # Find all threads that were started by our Machines
        threads_to_join = [
            thread for thread in threading.enumerate()
            if thread.name and thread.name.startswith("Machine-") # Filter by our naming convention
        ]

        for thread in threads_to_join:
            log_debug(f"Joining thread: {thread.name}")
            thread.join(timeout=10)
            if thread.is_alive():
                log_error(f"Thread {thread.name} did not terminate gracefully within timeout.")
            else:
                log_success(f"Thread {thread.name} terminated.") # Confirm successful join

    else:
        log_error("Inquisitor object was not fully initialized. Cannot perform graceful shutdown of capture threads.")

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
		safe_exit(inquisitor)
	except Exception as e:
		log_error(f"Fail in main loop :\t{e}")

	return 0

if __name__ == "__main__":
    print()
    log_info("Starting ARP monitor...\n")	
    main()
    print()
