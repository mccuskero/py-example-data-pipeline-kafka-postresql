# TODO

This is an example of TODO.md

View the raw content of this file to understand the format.

## Todo

- [ ] stub the classifer API, return output, randomaly, but from list
- [ ] Research if multiple pyproject.tomls are needed per app... or just use 1
- [ ] Link in files from github e.g. TODO.md, docs dir, containing a RUNBOOK.md file?
- [ ] Create helm chart to install on local/laptop/server k3s cluster
- [ ] use asyncio, for consumer
- [ ] Work on kafka messaging consumer, protobuf, and asyncio
  - [ ] need to define how the ingestor will work, from file, or kafka
- [ ] Work on integrating unit testing into framework
  - [ ] integrate tox and uv
  - [ ] use a docker image to test
- [ ] Observability

### In Progress

- [x] Rename clf_test_classifier to classifier
- [x] query classifier api, and get results store in protobuf
- [x] store to postgres

### Done ✓

- [x] Create github repo (watch the name! change to postgresql)
- [x] Create my first TODO.md
- [x] standup stubbed services
  - [x] flw_1_ingestor
  - [x] flw_2_preprocessor
  - [x] and the rest...
- [x] Add in postgresql with database, using startup script
- [x] setup to use the py-ml-pytorch-iris-uv-docker project
  - [x] update the docker-compose to use the image create there to start up
  - [x] remove the dir here...
  - [x] Work on kafka messaging consumer, protobuf, and asyncio
  - [x] pass in env variables from Makefile, to Dockerfile
  - [x] pass in base image from Makefile...
  - [x] create consumer in ingester to create events
  - [x] Move producer and consumer to src/kafka
- [x] Create Ingester class, and use in main
- [x] Rename clf_test_handler to _classifier
- [x] Create topic in code... (if it doesn't exist, maybe add the fw. back in)
- [x] Work on kafka messaging consumer, protobuf, and asyncio
  - [x] create mock data generator
  - [x] send data to a speciic topic (monitor topic?)
  - [x] have consumer read in messages, print out, and pass on to another topic
  - [x] Goal is to go end to end, less insert to postgress
- [x] Work on integrating unit testing into framework
  - [x] Integrate a single unit test for probuf message
  - [x] Integrate serialize, deserialize
- [x] create protobuf and send events through pipeline
