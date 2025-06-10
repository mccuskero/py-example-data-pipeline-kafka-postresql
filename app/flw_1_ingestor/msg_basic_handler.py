import os
import sys
from datetime import datetime
from loguru import logger
from pprint import pformat
from google.protobuf.timestamp_pb2 import Timestamp

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList, IrisFeaturesIngestedList, IrisFeaturesIngested
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
        
        # processing data is simple, for now, just added created_at
        iris_feature_list_ingested = IrisFeaturesIngestedList()
        for iris_feature in iris_features_list.iris_features_list:
            iris_feature_ingested = IrisFeaturesIngested(
                received_at=Timestamp().GetCurrentTime(),
                iris_features=IrisFeatures(
                    sepal_length=iris_feature.sepal_length,
                    sepal_width=iris_feature.sepal_width,
                    petal_length=iris_feature.petal_length,
                    petal_width=iris_feature.petal_width
                )
            )
            iris_feature_list_ingested.iris_features_ingested.append(iris_feature_ingested)
        
        # logger.info(iris_feature_list_ingested)
        
        self.msg_producer.produce(iris_feature_list_ingested.SerializeToString())
    
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
    
