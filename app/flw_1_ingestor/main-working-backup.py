import time
import os
import sys
import json
import logging
from loguru import logger
from pprint import pformat
from msg_consumer import MsgConsumer
from msg_basic_handler import MsgHandler

def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    logger.info(f"KAFKA Stats: {pformat(stats_json)}")

def main():
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    stats_interval_ms = os.environ.get("KAFKA_STATS_INTERVAL_MS")
    topic_from = os.environ.get("KAFKA_TOPIC_INGESTOR_FROM")
    topic_to = os.environ.get("KAFKA_TOPIC_INGESTOR_TO")
    
    # Split the string into a list of topics
    topics_list = [topic.strip() for topic in topic_from.split(',')] if topic_from else []

    logger.info(f"Starting consumer with receiving from topics: {topic_from}, sending to topics: {topic_to}")
    logger.info(f"KAFKA_BOOTSTRAP_SERVERS: {broker}")
    logger.info(f"KAFKA_GROUP_ID: {group}")
    logger.info(f"KAFKA_STATS_INTERVAL_MS: {stats_interval_ms}")
    
    # The handler will handle the message from topic_from and send to topic_to
    # from_topic is used to validate the message is from the correct topic
    # to_topic is used to send the message to the correct topic
    msg_handler = MsgHandler(broker, topic_from, topic_to)
    
    if logger.level == logging.DEBUG:
        msg_consumer = MsgConsumer(broker, group, topics_list, stats_interval_ms, stats_cb, msg_handler)
    else:
        msg_consumer = MsgConsumer(broker, group, topics_list, stats_interval_ms, None, msg_handler)
    
    try:
        logger.info("Starting message consumption")
        msg_consumer.consume()
        logger.info("Message consumption completed")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        msg_consumer.close()

if __name__ == "__main__":
    main()
