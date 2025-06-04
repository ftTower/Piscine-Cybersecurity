.SILENT:

NAME = spider.py

.PHONY: run clean

run:
	@while read url; do \
		python3 $(NAME) "$$url"; \
	done < scrapSite.txt

clean:
	rm -rf .data/*

re: clean run

