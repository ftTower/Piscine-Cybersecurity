PYTHON := python3
SCRIPT := ./core/main.py

.PHONY: run clean

clear:
	clear

run: clear
	$(PYTHON) $(SCRIPT) test test test test

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete






