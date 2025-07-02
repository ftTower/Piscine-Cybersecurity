
PYTHON_EXEC = python3
SCRIPT = vaccine.py

all: run

clear:
	@clear

run: clear
	$(PYTHON_EXEC) $(SCRIPT) https://demo.testfire.net/login.jsp

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