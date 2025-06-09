import os
import sys
from loguru import logger
from pprint import pformat

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeaturesList
from kafka.msg_producer import MsgProducer

class MsgHandler:
    def __init__(self, broker, from_topic, to_topic):
        self.msg = None
        self.broker = broker
        self.from_topic = from_topic
        self.to_topic = to_topic
        
        self.msg_producer = MsgProducer(broker, to_topic)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def __del__(self):
        pass
    
    def __str__(self):
        return pformat(self.msg)
    
    def __repr__(self):
        return pformat(self.msg)
    
    def __len__(self):
        return len(self.msg)
    
    def __getitem__(self, key):
        return self.msg[key]
    
    def __setitem__(self, key, value):
        self.msg[key] = value
    
    def __delitem__(self, key):
        del self.msg[key]
    
    def __iter__(self):
        return iter(self.msg)
    
    def __next__(self):
        return next(self.msg)
    
    def __contains__(self, item):
        return item in self.msg
    
    # TODO: this is the only stage specific proessing... 
    # Need to move producer to library
    def handle_iris_features_list(self, msg):
        iris_features_list = IrisFeaturesList()
        iris_features_list.ParseFromString(msg.value())
        logger.info(iris_features_list)
        self.msg_producer.produce(iris_features_list.SerializeToString())
    
    def handle(self, msg):
        logger.info(f"Handling message: {msg}")
        self.msg = msg
        try:
            logger.info(f"Handling message for topic {msg.topic()}: from topic is {self.from_topic}, to topic is {self.to_topic}")
            if self.msg.topic() == self.from_topic:
                self.handle_iris_features_list(self.msg)
            else:
                raise ValueError(f"Unknown topic: {self.msg.topic()}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            raise e
        finally:
            pass
    
