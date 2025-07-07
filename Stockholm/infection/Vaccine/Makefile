
.SILENT:

LAB_PATH = lab

clear:
	clear

labs:
	git clone https://github.com/yuyudhn/SQLi-Labs-Docker.git $(LAB_PATH)/SQLi-Labs-Docker || true
	rm $(LAB_PATH)/SQLi-Labs-Docker/docker-compose.yml
	cp $(LAB_PATH)/docker-compose.yml $(LAB_PATH)/SQLi-Labs-Docker/
	cd $(LAB_PATH)/SQLi-Labs-Docker && docker-compose up --build -d

clean_labs:
	if [ -d "$(LAB_PATH)/SQLi-Labs-Docker" ]; then \
		cd $(LAB_PATH)/SQLi-Labs-Docker && docker-compose down; \
		cd ../../ && rm -rf $(LAB_PATH)/SQLi-Labs-Docker; \
	fi

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

run: clear
	python3 ./core/vaccine.py http://localhost:1338/

fclean: clean clean_labs clear
	echo "Finished cleaning bye bye"


re : clean clean_labs labs run