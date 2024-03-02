SERVER_DIR := fastapi
SERVER_HOST := 0.0.0.0
SERVER_PORT := 8000
SERVER_RELOAD := --reload

UI_DIR := frontend

DB_DIR := postgres
DB_CONTAINER_NAME := db

all: clean_db
	docker-compose up

clean_db:
	-docker stop $(DB_CONTAINER_NAME)
	-docker rm $(DB_CONTAINER_NAME)

ui_dev: ui_install
	cd $(UI_DIR); npm run dev

ui_prod: ui_install
	cd $(UI_DIR); npm run build
	cd $(UI_DIR); npm run start	

ui_install:
	cd $(UI_DIR); npm install

install: 
	cd $(UI_DIR); npm install