import os
import sys
from loguru import logger
from basic_msg_handler import MsgHandler

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from kafka.msg_consumer import MsgConsumer

class Classifier:
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
        logger.info(f"Starting classifier with broker: {self.broker}, group: {self.group}, topic_from: {self.topic_from}, topic_to: {self.topic_to}, topics_list: {self.topics_list}, stats_interval_ms: {self.stats_interval_ms}, stats_cb: {self.stats_cb}")
        
        try:
            self.msg_consumer.consume()
        except Exception as e:
            logger.error(f"Error running classifier: {e}")
        finally:
            self.msg_consumer.close()
        
    def close(self):
        pass
        
    