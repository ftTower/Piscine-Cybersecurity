
PYTHON_EXEC = python3
SCRIPT = vaccine.py
SCRIPT_PATH = ./core/

all: run

clear:
	@clear

run: clear
	$(PYTHON_EXEC) $(SCRIPT_PATH)$(SCRIPT) https://demo.testfire.net/login.jsp
	$(PYTHON_EXEC) $(SCRIPT_PATH)$(SCRIPT) http://testphp.vulnweb.com/login.php
clean:
	rm -rf __pycache__

victim:
	docker run -it -p 8050:80 vulnerables/web-dvwa
	
re:
	clean run

help:
	@echo "Available targets:"
	@echo "  run   - Execute the vaccine.py script"
	@echo "  clean - Remove temporary files"
	@echo "  help  - Show this help message"