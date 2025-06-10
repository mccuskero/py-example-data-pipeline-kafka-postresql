import os
import sys
from loguru import logger
from google.protobuf.timestamp_pb2 import Timestamp

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList, IrisFeaturesIngestedList, IrisFeaturesIngested, IrisFeaturesPreProcessedList, IrisFeaturesPreProcessed
from kafka.msg_producer import MsgProducer


class MsgHandler:
    def __init__(self, broker, from_topic, to_topic):
        self.broker = broker
        self.from_topic = from_topic
        self.to_topic = to_topic
        
        self.msg_producer = MsgProducer(broker, to_topic)
        
    def handle_iris_features_ingested_list(self, msg):
        iris_features_ingested_list = IrisFeaturesIngestedList()
        iris_features_ingested_list.ParseFromString(msg.value())
        logger.info(iris_features_ingested_list)
        
        # processing data is simple, for now, just added created_at
        iris_features_pre_processed_list = IrisFeaturesPreProcessedList()
        for iris_features_ingested in iris_features_ingested_list.iris_features_ingested:
            iris_features_pre_processed= IrisFeaturesPreProcessed(
                processed_at=Timestamp().GetCurrentTime(),
                sepal_length=iris_features_ingested.iris_features.sepal_length,
                sepal_width=iris_features_ingested.iris_features.sepal_width,
                petal_length=iris_features_ingested.iris_features.petal_length,
                petal_width=iris_features_ingested.iris_features.petal_width
            )
            iris_features_pre_processed_list.iris_features.append(iris_features_pre_processed)
        
        self.msg_producer.produce(iris_features_pre_processed_list.SerializeToString())
        
    def handle(self, msg):
        logger.info(f"Handling message for topic {msg.topic()}: from topic is {self.from_topic}, to topic is {self.to_topic}")
        
        try:
            if msg.topic() == self.from_topic:
                self.handle_iris_features_ingested_list(msg)
            else:
                raise ValueError(f"Unknown topic: {msg.topic()}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
        
        
        
        