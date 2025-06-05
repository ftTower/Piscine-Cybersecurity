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
	head -c 64 /dev/urandom | xxd -p | tr -d '\n' > key.hex
	$(PYTHON) $(SCRIPT) -g key.hex

k  : 
	$(PYTHON) $(SCRIPT) -k ft_otp.key


all : g k

.PHONY: run