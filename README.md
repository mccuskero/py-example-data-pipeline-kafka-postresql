# py-example-data-pipeline-kafka-postgresql project

This project is a skelaton project used as a sandbox to create data pipelines in python, for research and then to scale out. 

## building

### uv lock file

create lock file

```shell
uv lock
```

### buildng images per application stub

```shell

```

## Running

```shell
make run
```

Kafka and postgresql will take a few min, 1-2 to start (based on capacity of your docker env). After they are initialized you will see the following in the logs:

```shell
flw-clf-test-api-1        | 2025-05-23 16:02:51.223 | INFO     | __main__:main:5 - starting flw-clf-test-api
flw-4-postprocessor-1     | 2025-05-23 16:02:51.728 | INFO     | __main__:main:5 - starting flw-4-postprocessor
flw-3-clf-test-handler-1  | 2025-05-23 16:02:52.168 | INFO     | __main__:main:5 - starting flw-3-clf-test-handler
flw-2-preprocessor-1      | 2025-05-23 16:02:52.516 | INFO     | __main__:main:5 - starting flw-2-preprocessor
flw-1-ingestor-1          | 2025-05-23 16:02:52.866 | INFO     | __main__:main:5 - starting flw-1-ingestor
```

## Testing

To test out a python application locally from commandline

```shell

```
