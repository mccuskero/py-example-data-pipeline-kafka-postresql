import time
import os
import sys
import json
import logging
from loguru import logger
from confluent_kafka import Consumer, KafkaException
from pprint import pformat
from msg_consumer import MsgConsumer
from msg_basic_handler import MsgHandler

def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    logger.info(f"KAFKA Stats: {pformat(stats_json)}")

def main():
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    # topics = os.environ.get('KAFKA_TOPICS', 'topic1,topic2,topic3').split(',')
    topics = os.environ.get("KAFKA_TOPICS").split(',')
    stats_interval_ms = os.environ.get("KAFKA_STATS_INTERVAL_MS")
    mock_data_topic = os.environ.get("KAFKA_MOCK_DATA_TOPIC")
    
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {'bootstrap.servers': broker, 'group.id': group, 'session.timeout.ms': 6000,
            'auto.offset.reset': 'earliest', 'enable.auto.offset.store': False}
    conf['statistics.interval.ms'] = int(stats_interval_ms)
    
    if logger.level == logging.DEBUG:
        conf['stats_cb'] = stats_cb

    logger.info(f"Starting consumer with config: {conf}, and topics: {topics}")
    logger.info(f"KAFKA_BOOTSTRAP_SERVERS: {broker}")
    logger.info(f"KAFKA_GROUP_ID: {group}")
    logger.info(f"KAFKA_TOPICS: {topics}")
    logger.info(f"KAFKA_STATS_INTERVAL_MS: {stats_interval_ms}")

    # TODO: need to handle multiple topics... 
    # currently only handles one topic, using one handler... 
    # should be able to pass in multiple handlers to a consumer... 
    msg_handler = MsgHandler(mock_data_topic)
    
    if logger.level == logging.DEBUG:
        msg_consumer = MsgConsumer(broker, group, topics, stats_interval_ms, stats_cb, msg_handler)
    else:
        msg_consumer = MsgConsumer(broker, group, topics, stats_interval_ms, None, msg_handler)
    
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
