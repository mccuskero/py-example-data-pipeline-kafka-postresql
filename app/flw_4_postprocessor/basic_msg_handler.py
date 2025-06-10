import os
import sys
from loguru import logger

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeaturesClassifiedList, IrisFeaturesClassified


class MsgHandler:
    def __init__(self, broker, from_topic, to_topic):
        self.broker = broker
        self.from_topic = from_topic
        self.to_topic = to_topic
                
    def handle_iris_features_classified_list(self, msg):
        iris_features_classified_list = IrisFeaturesClassifiedList()
        iris_features_classified_list.ParseFromString(msg.value())
        logger.info(iris_features_classified_list)
        # TODO: store data in database
        
    def handle(self, msg):
        logger.info(f"Handling message for topic {msg.topic()}: from topic is {self.from_topic}, to postgresql")
        
        try:
            if msg.topic() == self.from_topic:
                self.handle_iris_features_classified_list(msg)
            else:
                raise ValueError(f"Unknown topic: {msg.topic()}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
        