.SILENT:

PYTHON := python3
SCRIPT := otp-generator.py
ARGV   := -g key.hex

clear:
	clear

run: clear
	@$(PYTHON) $(SCRIPT) $(ARGV)

g  : clear
	rm -f key.hex
	touch key.hex
	head -c 64 /dev/urandom | xxd -p > key.hex
	$(PYTHON) $(SCRIPT) -g key.hex

k  : clear
	$(PYTHON) $(SCRIPT) -k "$(shell head -c 10 /dev/urandom | tr -dc '[:print:]')"


.PHONY: run