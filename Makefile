.PHONY: build

build:
	docker-compose build app

push:
	docker-compose push app

up:
	docker-compose up -d app