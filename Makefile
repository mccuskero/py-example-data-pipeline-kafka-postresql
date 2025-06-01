# py-example-data-pipeline-kafka-postgres

# Project: flw-1-ingestor
PROJECT_NAME := flw-1-ingestor
# internal project names
DOCKERFILE_INGESTOR := Dockerfile.flw_1_ingestor
DOCKERFILE_PREPROCESSOR := Dockerfile.flw_2_preprocessor
DOCKERFILE_CLF_TEST_HANDLER := Dockerfile.flw_3_clf_test_handler
DOCKERFILE_POSTPROCESSOR := Dockerfile.flw_4_postprocessor
export PROJECT_NAME_INGESTOR := flw-1-ingestor
export PROJECT_NAME_PREPROCESSOR := flw-2-preprocessor
export PROJECT_NAME_CLF_TEST_HANDLER := flw-3-clf-test-handler
export PROJECT_NAME_POSTPROCESSOR := flw-4-postprocessor
# Project: py-pytorch-clf-api is created from another project located at: https://github.com/mccuskero/py-ml-pytorch-iris-uv-docker
export ClF_PROJECT_NAME := py-pytorch-clf-api

# kafka env variables
export KAFKA_BOOTSTRAP_SERVERS := kafka:9092
export KAFKA_GROUP_ID := flw
export KAFKA_TOPICS := 'flower_events'
export KAFKA_STATS_INTERVAL_MS := 1000

# protobuff env variables
export PROTO_PATH := protos
export PROTO_FILE := iris_feature_msgs.proto
export PROTO_OUT_DIR := src

# protoc commands
# NOTE: that the "-I" is needed to remove "protos" from the output dir creation
protoc-all:
	protoc  -I $(PROTO_PATH) --python_out=$(PROTO_OUT_DIR) $(PROTO_PATH)/**/*.proto

# docker commands for flw-1-ingestor
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

# docker commands for flw-2-preprocessor
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

# docker commands for flw-3-clf-test-handler
docker-build-flw-3-clf-test-handler:
	docker build -f $(DOCKERFILE_CLF_TEST_HANDLER) -t $(PROJECT_NAME_CLF_TEST_HANDLER):latest .

run-flw-3-clf-test-handler:
	docker run --name $(PROJECT_NAME_CLF_TEST_HANDLER) -p 8000:8000 $(PROJECT_NAME_CLF_TEST_HANDLER):latest

rm-flw-3-clf-test-handler:
	docker rm $(PROJECT_NAME_CLF_TEST_HANDLER)

stop-flw-3-clf-test-handler:
	docker stop $(PROJECT_NAME_CLF_TEST_HANDLER)

shell-flw-3-clf-test-handler:
	docker run -it --rm $(PROJECT_NAME_CLF_TEST_HANDLER):latest /bin/bash

attach-flw-3-clf-test-handler:
	docker exec -it $(PROJECT_NAME_CLF_TEST_HANDLER) /bin/bash

# docker commands for flw-4-postprocessor
docker-build-flw-4-postprocessor:
	docker build -f $(DOCKERFILE_POSTPROCESSOR) -t $(PROJECT_NAME_POSTPROCESSOR):latest .

run-flw-4-postprocessor:
	docker run --name $(PROJECT_NAME_POSTPROCESSOR) -p 8000:8000 $(PROJECT_NAME_POSTPROCESSOR):latest

rm-flw-4-postprocessor:
	docker rm $(PROJECT_NAME_POSTPROCESSOR)

stop-flw-4-postprocessor:
	docker stop $(PROJECT_NAME_POSTPROCESSOR)

shell-flw-4-postprocessor:
	docker run -it --rm $(PROJECT_NAME_POSTPROCESSOR):latest /bin/bash

attach-flw-4-postprocessor:
	docker exec -it $(PROJECT_NAME_POSTPROCESSOR) /bin/bash

# run the data pipeline
run:
	@docker-compose up -d

# run the data pipeline
build-and-run: docker-build-flw-1-ingestor \
	docker-build-flw-2-preprocessor \
	docker-build-flw-3-clf-test-handler \
	docker-build-flw-4-postprocessor
	@docker-compose up -d
#	@docker-compose up

logs:
	@docker-compose logs -f

stop:
	@docker-compose down

# run the tests
test-protobuf: protoc-all
	@pytest tests/protobuf/test_ingestor_messages.py

# run the tests, including the protobuf files
test-all: test-protobuf

# clean up all the docker images and containers
clean:
	@rm -f docker-build*

clean-all:
	@make clean
	@make clean-images

clean-images:
	@docker system prune -a --filter label=project-name="$(PROJECT_NAME)" -f

# extra clean commands
clean-all-images:
	@docker system prune -a -f

clean-all-containers:
	@docker system prune -f

clean-all-volumes:
	@docker system prune -a -f

clean-all-networks:
	@docker system prune -a -f