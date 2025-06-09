import os
import sys
import time
from loguru import logger

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList
from kafka.msg_producer import MsgProducer


class MockDataGenerator:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic        
        self.producer = MsgProducer(broker, topic)
        
    def generate_mock_data(self):
        iris_features_list = IrisFeaturesList()
        iris_features_list.iris_features_list.append(IrisFeatures(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
        iris_features_list.iris_features_list.append(IrisFeatures(sepal_length=6.1, sepal_width=4.5, petal_length=2.4, petal_width=1.2))
        return iris_features_list

    def delivery_report(err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    def generate(self): 
        logger.info(f"Starting mock data generator with broker: {self.broker}, topic: {self.topic}")
        try:
            logger.info(f"Generating mock data and sending to topic: {self.topic}")
            while True:
                iris_features_list = self.generate_mock_data()
                logger.info(f"Sending mock data to topic: {self.topic}")
                self.producer.produce(iris_features_list.SerializeToString())
                time.sleep(1)
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {e}")
        finally:
            self.producer.flush()
            self.producer.close()
            logger.info(f"Mock data generator completed")
            
    def close(self):
       pass
            