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

from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList


class MsgHandler:
    def __init__(self, target_topic):
        self.msg = None
        self.target_topic = target_topic

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
    
    def handle(self, msg):
        logger.info(f"Handling message: {msg}")
        self.msg = msg
        try:
            logger.info(f"Handling message for topic {msg.topic()}: target topic is {self.target_topic}")
            # TODO: how to handle multiple topics? 
            # currently only handles one topic, using one handler... 
            # should be able to pass in multiple handlers to a consumer... 
            if self.msg.topic() == self.target_topic:
                iris_features_list = IrisFeaturesList()
                iris_features_list.ParseFromString(self.msg.value())
                logger.info(iris_features_list)
            # elif self.msg.topic() == 'iris_features':
            #     iris_features = IrisFeatures()
            #     iris_features.ParseFromString(self.msg.value())
            #     print(iris_features)
            # elif self.msg.topic() == 'iris_features_list':
            #     iris_features_list = IrisFeaturesList()
            #     iris_features_list.ParseFromString(self.msg.value())
            #     print(iris_features_list)
            else:
                raise ValueError(f"Unknown topic: {self.msg.topic()}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            raise e
        finally:
            pass
    
