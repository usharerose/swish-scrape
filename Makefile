.PHONY: clean-pyc

build: clean-pyc
	bash ./scripts/generate-procfile-prod.sh
	docker-compose build swish-scrape-build

run: build clean-container
	docker-compose up -d swish-scrape-run

ssh:
	docker-compose exec swish-scrape-run bash

clean-pyc:
	# clean all pyc files
	find . -name '__pycache__' | xargs rm -rf | cat
	find . -name '*.pyc' | xargs rm -f | cat

clean-container:
	# stop and remove useless containers
	docker-compose down --remove-orphans
