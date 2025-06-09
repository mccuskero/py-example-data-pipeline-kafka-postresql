#!/bin/bash

# Assume KAFKA_CREATE_TOPICS is set like: export KAFKA_CREATE_TOPICS="topic1,topic2,topic3"
# TODO:  someday add in paramerers and rep factor... KAFKA_CREATE_TOPICS: "my_topic_1:1:1,my_topic_2:3:1,another_topic:1:3"
echo "KAFKA_CREATE_TOPICS: ${KAFKA_CREATE_TOPICS}"
echo "KAFKA_BOOTSTRAP_SERVERS: ${KAFKA_BOOTSTRAP_SERVERS}"

echo "Creating topics..."
IFS=',' read -ra ADDR <<< "$KAFKA_CREATE_TOPICS"
for topic in "${ADDR[@]}"; do
  echo "Creating topic: $topic"
  /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topic" --bootstrap-server $KAFKA_BOOTSTRAP_SERVERS --partitions 1 --replication-factor 1
done
echo "Topics created"
