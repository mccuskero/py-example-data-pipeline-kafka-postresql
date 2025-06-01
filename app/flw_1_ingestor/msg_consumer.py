import os
import sys
import json
import logging
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
        self.consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        })  

        if self.stats_interval_ms:
            self.consumer.subscribe(self.topics)
        if self.stats_cb:
            self.consumer.set_stats_cb(self.stats_cb)

        self.consumer.subscribe(self.topics)

    def consume(self, callback=None):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                if self.msg_handler:
                    self.msg_handler.handle(msg)
                else:
                    if callback:
                        callback(msg)
                yield msg
        except KeyboardInterrupt:
            pass
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