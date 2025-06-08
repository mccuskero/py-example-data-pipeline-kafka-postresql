import time
import os
import sys
import json
import logging
from loguru import logger
from confluent_kafka import Consumer, KafkaException
from pprint import pformat


def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    logger.info(f"KAFKA Stats: {pformat(stats_json)}")

def print_usage_and_exit(program_name):
    sys.stderr.write('Usage: %s [options..] <bootstrap-brokers> <group> <topic1> <topic2> ..\n' % program_name)
    options = '''
 Options:
  -T <intvl>   Enable client statistics at specified interval (ms)
'''
    sys.stderr.write(options)
    sys.exit(1)

def main():
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    # topics = os.environ.get('KAFKA_TOPICS', 'topic1,topic2,topic3').split(',')
    topics = os.environ.get("KAFKA_TOPICS").split(',')
    stats_interval_ms = os.environ.get("KAFKA_STATS_INTERVAL_MS")
    
    # Create logger for consumer (logs will be emitted when poll() is called)
    #logger = logging.getLogger('consumer')
    #logger.setLevel(logging.DEBUG)
    #handler = logging.StreamHandler()
    #handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    #logger.addHandler(handler)

    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {'bootstrap.servers': broker, 'group.id': group, 'session.timeout.ms': 6000,
            'auto.offset.reset': 'earliest', 'enable.auto.offset.store': False}
    conf['statistics.interval.ms'] = int(stats_interval_ms)
    conf['stats_cb'] = stats_cb

    logger.info(f"Starting consumer with config: {conf}, and topics: {topics}")
    logger.info(f"KAFKA_BOOTSTRAP_SERVERS: {broker}")
    logger.info(f"KAFKA_GROUP_ID: {group}")
    logger.info(f"KAFKA_TOPICS: {topics}")
    logger.info(f"KAFKA_STATS_INTERVAL_MS: {stats_interval_ms}")


    # Create Consumer instance
    # Hint: try debug='fetch' to generate some log messages
    c = Consumer(conf, logger=logger)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

    # Subscribe to topics
    c.subscribe(topics, on_assign=print_assignment)

    # Read messages from Kafka, print to stdout
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                print(msg.value())
                # Store the offset associated with msg to a local cache.
                # Stored offsets are committed to Kafka by a background thread every 'auto.commit.interval.ms'.
                # Explicitly storing offsets after processing gives at-least once semantics.
                c.store_offsets(msg)

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        # Close down consumer to commit final offsets.
        c.close()
        
if __name__ == "__main__":
    main()
