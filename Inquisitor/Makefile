PYTHON := python3
SCRIPT := ./core/main.py

.PHONY: run clean

clear:
	clear

run: clear
	$(PYTHON) $(SCRIPT) 1.1.1.1 00:1A:2B:3C:4D:5E 1.1.1.1 00:1A:2B:3C:4D:5E

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete






