.PHONY: build

build:
	docker-compose build app

up:
	docker-compose up -d app