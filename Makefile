# py-example-data-pipeline-kafka-postgres

# Project: flw-1-ingestor
PROJECT_NAME := flw-1-ingestor
# internal project names
DOCKERFILE_MOCK_DATA_GENERATOR := Dockerfile.flw_0_mock_data_generator
DOCKERFILE_INGESTOR := Dockerfile.flw_1_ingestor
DOCKERFILE_PREPROCESSOR := Dockerfile.flw_2_preprocessor
DOCKERFILE_CLF_TEST_HANDLER := Dockerfile.flw_3_clf_test_handler
DOCKERFILE_POSTPROCESSOR := Dockerfile.flw_4_postprocessor
export PROJECT_NAME_MOCK_DATA_GENERATOR := flw-0-mock-data-generator
export PROJECT_NAME_INGESTOR := flw-1-ingestor
export PROJECT_NAME_PREPROCESSOR := flw-2-preprocessor
export PROJECT_NAME_CLF_TEST_HANDLER := flw-3-clf-test-handler
export PROJECT_NAME_POSTPROCESSOR := flw-4-postprocessor
# Project: py-pytorch-clf-api is created from another project located at: https://github.com/mccuskero/py-ml-pytorch-iris-uv-docker
export ClF_PROJECT_NAME := py-pytorch-clf-api

# kafka env variables
export KAFKA_BOOTSTRAP_SERVERS := kafka:9092
export KAFKA_GROUP_ID := flw
export KAFKA_STATS_INTERVAL_MS := 1000
# TODO: need to include parameters sometime... 
export KAFKA_CREATE_TOPICS := fw.ingestor.features.list.event,fw.preprocessor.features.list.event,fw.classifier.features.list.event,fw.postprocessor.features.list.event

export KAFKA_TOPIC_MOCK_DATA_GENERATOR_TO := fw.ingestor.features.list.event
export KAFKA_TOPIC_INGESTOR_FROM := fw.ingestor.features.list.event
export KAFKA_TOPIC_INGESTOR_TO := fw.preprocessor.features.list.event
export KAFKA_TOPIC_PREPROCESSOR_FROM := fw.preprocessor.features.list.event
export KAFKA_TOPIC_PREPROCESSOR_TO := fw.classifier.features.list.event
export KAFKA_TOPIC_CLASSIFIER_FROM := fw.classifier.features.list.event
export KAFKA_TOPIC_CLASSIFIER_TO := fw.postprocessor.features.list.event
export KAFKA_TOPIC_POSTPROCESSOR_FROM := fw.postprocessor.features.list.event
# NOTE: Postprocessor save data to postgres

# protobuff env variables
export PROTO_PATH := protos
export PROTO_FILE := iris_feature_msgs.proto
export PROTO_OUT_DIR := src

# protoc commands
# NOTE: that the "-I" is needed to remove "protos" from the output dir creation
protoc-all:
	protoc  -I $(PROTO_PATH) --python_out=$(PROTO_OUT_DIR) $(PROTO_PATH)/**/*.proto

# docker commands for flw-0-mock-data-generator
docker-build-flw-0-mock-data-generator:
	docker build -f $(DOCKERFILE_MOCK_DATA_GENERATOR) -t $(PROJECT_NAME_MOCK_DATA_GENERATOR):latest .

run-flw-0-mock-data-generator: rm-flw-0-mock-data-generator
	docker run --init -it --env-file .env-dev --name $(PROJECT_NAME_MOCK_DATA_GENERATOR) $(PROJECT_NAME_MOCK_DATA_GENERATOR):latest

rm-flw-0-mock-data-generator:
	-docker rm $(PROJECT_NAME_MOCK_DATA_GENERATOR) || true

stop-flw-0-mock-data-generator:
	docker stop $(PROJECT_NAME_MOCK_DATA_GENERATOR)

shell-flw-0-mock-data-generator:
	docker run -it --rm $(PROJECT_NAME_MOCK_DATA_GENERATOR):latest /bin/bash

attach-flw-0-mock-data-generator:
	docker exec -it $(PROJECT_NAME_MOCK_DATA_GENERATOR) /bin/bash

# docker commands for flw-1-ingestor
docker-build-flw-1-ingestor:
	docker build -f $(DOCKERFILE_INGESTOR) -t $(PROJECT_NAME_INGESTOR):latest .

run-flw1-ingestor:
	docker run --env-file .env-dev --name $(PROJECT_NAME_INGESTOR) $(PROJECT_NAME_INGESTOR):latest

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

run-flw-2-preprocessor: rm-flw-2-preprocessor
	docker run --env-file .env-dev --name $(PROJECT_NAME_PREPROCESSOR) $(PROJECT_NAME_PREPROCESSOR):latest

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
	docker run --env-file .env-dev --name $(PROJECT_NAME_CLF_TEST_HANDLER) $(PROJECT_NAME_CLF_TEST_HANDLER):latest

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
	docker run --env-file .env-dev --name $(PROJECT_NAME_POSTPROCESSOR) $(PROJECT_NAME_POSTPROCESSOR):latest

rm-flw-4-postprocessor:
	docker rm $(PROJECT_NAME_POSTPROCESSOR)

stop-flw-4-postprocessor:
	docker stop $(PROJECT_NAME_POSTPROCESSOR)

shell-flw-4-postprocessor:
	docker run -it --rm $(PROJECT_NAME_POSTPROCESSOR):latest /bin/bash

attach-flw-4-postprocessor:
	docker exec -it $(PROJECT_NAME_POSTPROCESSOR) /bin/bash

# kafka test
run-kafka-test:
	@docker-compose -f docker-compose-kafka.yml up

shell-kafka-test:
	@docker-compose -f docker-compose-kafka.yml exec kafka /bin/bash

logs-kafka-test:
	@docker-compose -f docker-compose-kafka.yml logs -f

stop-kafka-test:
	@docker-compose -f docker-compose-kafka.yml down

# run the data pipeline
run:
	@docker-compose up -d

# run the data pipeline
build-and-run: docker-build-flw-0-mock-data-generator \
    docker-build-flw-1-ingestor \
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