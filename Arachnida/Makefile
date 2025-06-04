.SILENT:

NAME = spider.py

.PHONY: run clean

run:
	echo
	@while read url; do \
		python3 $(NAME) -r "$$url"; \
	done < scrapSite.txt
	echo

clean:
	rm -rf .data/*

clear:
	clear

re: clear clean run

