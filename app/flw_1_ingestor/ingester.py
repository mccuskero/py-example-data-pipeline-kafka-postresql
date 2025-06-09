import os
import sys
from loguru import logger

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from kafka.msg_consumer import MsgConsumer

from msg_basic_handler import MsgHandler

class Ingester:
    def __init__(self, broker, group, topic_from, topic_to, topics_list, stats_interval_ms, stats_cb):
        self.broker = broker
        self.group = group
        self.topic_from = topic_from
        self.topic_to = topic_to
        self.topics_list = topics_list
        self.stats_interval_ms = stats_interval_ms
        self.stats_cb = stats_cb
        
        self.msg_handler = MsgHandler(broker, topic_from, topic_to)
        self.msg_consumer = MsgConsumer(broker, group, topics_list, stats_interval_ms, stats_cb, self.msg_handler)
        
    def run(self):
        logger.info(f"Starting ingester with broker: {self.broker}, \
            group: {self.group}, topic_from: {self.topic_from}, topic_to: {self.topic_to}, \
            topics_list: {self.topics_list}, stats_interval_ms: {self.stats_interval_ms}, stats_cb: {self.stats_cb}")
        
        try:
            logger.info("Starting message consumption")
            self.msg_consumer.consume()
            logger.info("Message consumption completed")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            self.close()
        
    def close(self):
        self.msg_consumer.close()
        self.msg_handler.close()