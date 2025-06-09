import json
from loguru import logger
from confluent_kafka import Consumer, KafkaException
from pprint import pformat  # noqa: F401


class MsgConsumer:
    def __init__(self, bootstrap_servers, group_id, topics, stats_interval_ms=None, stats_cb=None, msg_handler=None):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topics = topics
        self.stats_interval_ms = stats_interval_ms
        self.stats_cb = stats_cb
        self.msg_handler = msg_handler
        self.conf = None
        # Create the consumer configuration
        self.conf = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }

        if self.stats_interval_ms:
            self.conf['statistics.interval.ms'] = self.stats_interval_ms
        if self.stats_cb:
            self.conf['stats_cb'] = self.stats_cb
        
        self.consumer = Consumer(self.conf)  
        self.consumer.subscribe(self.topics)

    def consume(self, callback=None):
        logger.info(f"Consuming messages from {self.topics} with config: {self.conf}")
        try:
            while True:
                logger.info("Polling for messages")
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    logger.info("No message received")
                    continue
                if msg.error():
                    logger.error(f"Error polling for messages: {msg.error()}")
                    raise KafkaException(msg.error())
                else:
                    logger.info("Message received")
                    logger.info(msg.value())
                    logger.info("Calling message handler")
                    self.msg_handler.handle(msg)
                # if self.msg_handler:
                #     logger.info("Handling message")
                #     self.msg_handler.handle(msg)
                # else:
                #     logger.info("No message handler provided")
                #     if callback:
                #         logger.info("Calling callback")
                #         callback(msg)
                #     else:
                #         logger.info("No callback provided")
#                yield msg
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Exiting...")
        finally:
            self.close()

    def stats_cb(self, stats_json_str):
        stats_json = json.loads(stats_json_str)
        logger.info(f"KAFKA Stats: {pformat(stats_json)}")  

    def close(self):
        if self.consumer:
            self.consumer.close()
            self.consumer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == "__main__":
    consumer = MsgConsumer(
        bootstrap_servers="localhost:9092",
        group_id="test-group",
        topics=["test-topic"],
    )