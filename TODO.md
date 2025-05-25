# TODO

This is an example of TODO.md

View the raw content of this file to understand the format.

## Todo

- [ ] stub the classifer API, return output, randomaly, but from list
- [ ] send results to postgresql
  - [ ] create a results protobuf to send to postproessor...
- [ ] Research if multiple pyproject.tomls are needed per app... or just use 1
- [ ] Link in files from github e.g. TODO.md, docs dir, containing a RUNBOOK.md file?
- [ ] Create helm chart to install on local/laptop/server k3s cluster

### In Progress

- [x] Work on kafka messaging, protobuf, and asyncio
- [x] create protobuf and send events through pipeline
  - [x] create mock data generator
  - [x] send data to a speciic topic (monitor topic?)

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
