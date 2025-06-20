# py-example-data-pipeline-kafka-postgresql project

This project is a skelaton project used as a sandbox to create data pipelines in python, for research and then to scale out.

IMPORTANT: This project uses an image from the following classifier api <https://github.com/mccuskero/py-ml-pytorch-iris-uv-docker>. You can build the image local to your docker enviroment. The docker-compose.yml file will use the project name to start it up.

## Overall Concepts

There are a number of challenges in developing and maintain a data pipeline that incorporates classifier APIs. Here are a few challenges listed:

- Managing version conflicting dependencies e.g. tensorflow vs protoc protobuf package.
- Establishing a pipeline architeture that can scale e.g. leverage docker images, kubernetes, protobuf, and kafka
- TBD

### Managing project with uv

You can add depedencies to the pyproject.toml file, and will need to run the uv lock, after the file us updated using the following:

```shell
uv lock
```

Note you can also use the following...

```shell
 uv add protobuf==5.29.3
```

You will see the uv.lock file getting updated.

### Passing in variables to Docker images

There are a number of ways to pass in environment variables to images, and different themes and variables to each. The two main ways are:

- When using docker run, you can use a .env file e.g. .env-dev
- When using docker compose, you can export them from the Makefile

### Kafka naming conventions

Kafka topic naming conventions aim for clarity, consistency, and organization. A common approach is a hierarchical structure, using periods or underscores to separate different levels of meaning. For example, sales.ecommerce.shoppingcarts.events. This could represent the "sales" domain, "ecommerce" subdomain, "shoppingcarts" context, and "events" data type.

### working with kafka externally

You will need to install kafka (brew install kafka)

For the kafka container to be seen from a commaind line, review the docker-compose.yml. The following was needed:
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092

Then you can do the following to test topics, from a command line...

```shell
➜  env kafka-topics --bootstrap-server localhost:9092 --create --topic my-test-topic
Created topic my-test-topic.
➜  env kafka-topics --bootstrap-server localhost:9092 --list
my-test-topic
```

To generate messages for a topic

```shell
kafka-console-producer --bootstrap-server localhost:9092 --topic fwevents
```

To consume in another window

```shell
kafka-consumer-groups --bootstrap-server localhost:9092
```

```shell
kafka-topics --bootstrap-server localhost:9092 --describe --topic fwevents
```

#### Testing just kafka

I created docker-compose-kafka.yml file to test connectivit with external command line, and a docker kafka container running within Rancher.

You can use the above kakfa cli tools to connect with it e.g. craete topics, send and receive messages.

#### .env-dev file

I created a env file to be read in from a docker run execution to setup different environmental variables. Note that, running the generator externally doesn't connect through yet. There are some connectivity issues.

### Managing multiple versions of libs e.g. protobuf conflicting dependencies

Machine learning packages have specific dependencies that may be needed to be locked in e.g. uv package managment tool. For example, tensorflow has a specific dependency associated with protobuf, and may differ from other components of the pipeline e.g. protobuf messaging using kafka.

For example, you may see this error when developing a tensorflow based classifier and message in the same venv.

```shell
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
tensorflow 2.16.2 requires protobuf!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<5.0.0dev,>=3.20.3, but you have protobuf 6.31.1 which is incompatible.
```

Then, on top of this, when running protoc against your proto files, you may see this error

```shell
Traceback (most recent call last):
  File "/Users/owenmccusker/Documents/repos-git/py-example-data-pipeline-kafka-postresql/tests/test_ingestor_messages.py", line 18, in <module>
    from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList
  File "/Users/owenmccusker/Documents/repos-git/py-example-data-pipeline-kafka-postresql/src/iris_features_pb/iris_features_pb2.py", line 9, in <module>
    from google.protobuf import runtime_version as _runtime_version
ImportError: cannot import name 'runtime_version' from 'google.protobuf' (/Users/owenmccusker/.pyenv/versions/3.10.12/lib/python3.10/site-packages/google/protobuf/__init__.py)
```

Which the following fixes:

```shell
 pip install --upgrade protobuf
```

But can lead to a warning, with protoc, where protoc tries to keep major version protobuf (in this case 5.29.3) in line with to installed pip library, which was  6.31.1.

```shell
➜  imports-paths-examples protoc --version
libprotoc 29.3

/Users/owenmccusker/.pyenv/versions/3.10.12/lib/python3.10/site-packages/google/protobuf/runtime_version.py:98: UserWarning: Protobuf gencode version 5.29.3 is exactly one major version older than the runtime version 6.31.1 at iris_features_pb/iris_features.proto. Please update the gencode to avoid compatibility violations in the next runtime release.
  warnings.warn(
```

When you generate a protobuf python file, _pb2,  you will see the following in the file denoted the protobuf library that protoc used:

```shell
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: iris_features_pb/iris_features.proto
# Protobuf Python Version: 5.29.3
```

Running the following fixed that:

```shell
pip install protobuf==5.29.3
```

#### Conclusions

To successfully manage these issues we need to develop a pattern to insulated each component from the other using a consistent development pattern. One  solutions assocaited with managing version descrepencies is to break apart components e.g. classifiers api, from the pipeline, building and deliverying them separately. What I have done is:

- Separate the classifiers out, from the data pipeline (kakfa, and protobuf messzges) into a separate monorepo for now (note different classifiers may have issues with one another)
- Ensure that kafka messaging and classifier api protobuf messages don't meet, pass in a "Class" or json string, into the classifier api.

## building

### uv lock file

create lock file

```shell
uv lock
```

### Building the protobuf files

This will need some work in the future, today, those files are built locally. To support this, the following has been installed on a Mac OS X

- setup a venv for your local work.
- protoc compiler (brew install protobuf)
- supporting protobuf python library  (pip install protobuf==5.29.3)

I incorporated a make command in the Makefile

```shell
# protoc commands
# NOTE: that the "-I" is needed to remove "protos" from the output dir creation
protoc-all:
    protoc  -I $(PROTO_PATH) --python_out=$(PROTO_OUT_DIR) $(PROTO_PATH)/**/*.proto
```

This will copy the dir structure (packages), from the protos dir, to under the src, without including the "protos" pathname.

### buildng images per application stub

```shell

```

## Running

This section covers how to run the complete pipeline from the docker compose file. NOTE: when doing just the "make run", we can get errors, when images are not found locally in your docker env (I use rancher, you will see something like docker login error). You can run "make build-and-run".

This project is dependent on a classifier api called: py-pytorch-clf-api. You can clone and install the image in your local docker env here: <https://github.com/mccuskero/py-ml-pytorch-iris-uv-docker>. You will see this image name referenced in the docker-compose.yml file, where ClF_PROJECT_NAME is defined in the Makefile as py-pytorch-clf-api.

```shell
# going to start up the pipeline backwards... to ensure we have a working pipeline
# starting with the py-pytorch-clf-api service
services:
  py-pytorch-clf-api:
    image: ${ClF_PROJECT_NAME}:latest
    depends_on:
      kafkasetup:
        condition: service_completed_successfully
    networks:
      - flw-pipeline-network
    ports:
      - 8000:8000
```

### Running and building the pipeline

Check to see if your classifier image is located in your docker repo:

```shell
➜ ✗ docker image ls py-pytorch-clf-api
REPOSITORY           TAG       IMAGE ID       CREATED      SIZE
py-pytorch-clf-api   latest    03aec70550f9   7 days ago   12.2GB
```

If so, then startup the pipeline line, this will run in the background.

```shell
make build-and-run
```

Then you can check out the logs from the services with:

```shell
make logs
```

Kafka and postgresql will take a few min, 1-2 to start (based on capacity of your docker env). After they are initialized you will see the following in the logs:

```shell
py-pytorch-clf-api-1        | 2025-05-23 16:02:51.223 | INFO     | __main__:main:5 - starting py-pytorch-clf-api
flw-4-postprocessor-1     | 2025-05-23 16:02:51.728 | INFO     | __main__:main:5 - starting flw-4-postprocessor
flw-3-clf-test-handler-1  | 2025-05-23 16:02:52.168 | INFO     | __main__:main:5 - starting flw-3-clf-test-handler
flw-2-preprocessor-1      | 2025-05-23 16:02:52.516 | INFO     | __main__:main:5 - starting flw-2-preprocessor
flw-1-ingestor-1          | 2025-05-23 16:02:52.866 | INFO     | __main__:main:5 - starting flw-1-ingestor
```

You should be able to reach the classifier api swagger page from the browser, <http://0.0.0.0:8000/docs>

## Testing

To test out a python application locally from commandline.

To support testing I installed the following, pytest 8.3.5, and added a simple pytest.ini file.

```shell
pip show pytest

Name: pytest
Version: 8.3.5
```

### Running tests

Tests are run from the Makeifle.

```shell
make test-all
```
