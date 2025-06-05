.SILENT:

PYTHON := python3
SCRIPT := otp-generator.py


HEXA_KEY_FILE := key.hex
CRYPTED_KEY_FILE := ft_otp.key

clear:
	clear

clean: clear
	rm -f $(HEXA_KEY_FILE)
	rm -f $(CRYPTED_KEY_FILE)

g  : clean
	rm -f $(HEXA_KEY_FILE)
	touch $(HEXA_KEY_FILE)
	head -c 64 /dev/urandom | xxd -p | tr -d '\n' > $(HEXA_KEY_FILE)
	$(PYTHON) $(SCRIPT) -g $(HEXA_KEY_FILE)

k  : 
	$(PYTHON) $(SCRIPT) -k $(CRYPTED_KEY_FILE)


all : g k

.PHONY: run