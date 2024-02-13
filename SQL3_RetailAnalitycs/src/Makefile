# @authors   bellatri (    --    )
#			 cgreenbe (    --    )
#			 pintoved (Pinto Veda)

TAG   	  	   		:= 15
REPOSITORY			:= 
IMAGE 	  	   		:= $(REPOSITORY)postgres:$(TAG)
CONTAINER 	   		:= PostgreSQL

PORT_CONTAINER 		:= 5432
PORT           		:= 5432

DOCKERFILE_DIR 		:= src
PROJECT_DIR         := $(shell pwd)/../

all: stop_container run_container

build_image: 
	docker build -t $(IMAGE) $(DOCKERFILE_DIR)

run_container:
	docker run \
	-it --rm --name $(CONTAINER) \
	-p $(PORT):$(PORT_CONTAINER) \
	-e POSTGRES_HOST_AUTH_METHOD=trust \
	$(IMAGE) 

# run_container:
# 	docker run \
# 	-it --rm --name $(CONTAINER) \
# 	-p $(PORT):$(PORT_CONTAINER) \
# 	--restart=no \
# 	--runtime=runc \
# 	--env=PG_MAJOR=15 \
# 	--env=LANG=en_US.utf8 \
# 	--hostname=a55622b77566 \
# 	--env=GOSU_VERSION=1.16 \
# 	--mac-address=02:42:ac:11:00:02 \
# 	--volume=$(PROJECT_DIR):/project/ \
# 	--env=PG_VERSION=15.1-1.pgdg110+1 \
# 	--volume=/var/lib/postgresql/data \
# 	--env=POSTGRES_PASSWORD=postgrespw \
# 	-d postgres \
# 	--env=PGDATA=/var/lib/postgresql/data \
# 	--label='com.docker/featured-image=postgres:latest' \
# 	--env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/postgresql/15/bin \
# 	$(IMAGE) 

stop_container:
	-docker stop $(CONTAINER)
	-docker rm $(CONTAINER)

delete_image: stop_container
	-docker rmi $(IMAGE)

# INFORMATION
info: 
	-docker ps
	-docker ps -a
	-docker images

connection:
	-curl localhost:$(PORT)

push:
	docker push $(IMAGE)

# run: my_image
# 	docker run -d -it -p 80:81 \
# 	-v /home/student/SimpleDocker/src/nginx/nginx.conf:/etc/nginx/nginx.conf \
# 	--name Eleott \
# 	my_image:server \



