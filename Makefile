# py-example-data-pipeline-kafka-postgres

# Project: flw-1-ingestor
PROJECT_NAME := flw-1-ingestor
DOCKERFILE_INGESTOR := Dockerfile.flw_1_ingestor
DOCKERFILE_PREPROCESSOR := Dockerfile.flw_2_preprocessor
export PROJECT_NAME_INGESTOR := flw-1-ingestor
export PROJECT_NAME_PREPROCESSOR := flw-2-preprocessor

# Dockerfile commands a new image with the build	
docker-build-flw-1-ingestor:
	docker build -f $(DOCKERFILE_INGESTOR) -t $(PROJECT_NAME_INGESTOR):latest .

run-flw1-ingestor:
	docker run --name $(PROJECT_NAME_INGESTOR) -p 8000:8000 $(PROJECT_NAME_INGESTOR):latest

rm-flw1-ingestor:
	docker rm $(PROJECT_NAME_INGESTOR)

stop-flw-1-ingestor:
	docker stop $(PROJECT_NAME_INGESTOR)

shell-flw-1-ingestor:
	docker run -it --rm $(PROJECT_NAME_INGESTOR):latest /bin/bash

attach-flw-1-ingestor:
	docker exec -it $(PROJECT_NAME_INGESTOR) /bin/bash

# docker commands for preprocessor
docker-build-flw-2-preprocessor:
	docker build -f $(DOCKERFILE_PREPROCESSOR) -t $(PROJECT_NAME_PREPROCESSOR):latest .

run-flw-2-preprocessor:
	docker run --name $(PROJECT_NAME_PREPROCESSOR) -p 8000:8000 $(PROJECT_NAME_PREPROCESSOR):latest

rm-flw-2-preprocessor:
	docker rm $(PROJECT_NAME_PREPROCESSOR)

stop-flw-2-preprocessor:
	docker stop $(PROJECT_NAME_PREPROCESSOR)

shell-flw-2-preprocessor:
	docker run -it --rm $(PROJECT_NAME_PREPROCESSOR):latest /bin/bash

attach-flw-2-preprocessor:
	docker exec -it $(PROJECT_NAME_PREPROCESSOR) /bin/bash

# run the data pipeline
run: docker-build-flw-1-ingestor docker-build-flw-2-preprocessor
	@docker-compose up

# clean up all the docker images and containers
clean:
	@rm -f docker-build*

clean-all:
	@make clean
	@make clean-images

clean-images:
	@docker system prune -a --filter label=project-name="$(PROJECT_NAME)" -f