import sys
import os
import time
import signal
from confluent_kafka import Producer
from loguru import logger

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from iris_features_pb.iris_features_pb2 import IrisFeatures, IrisFeaturesList

#KAFKA_TOPIC = 'iris-features'
#KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

def handle_signals(signum, frame):
    logger.info(f"Signal {signum} received. Exiting...")
    sys.exit(0)
    
signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)

def generate_mock_data():
    iris_features_list = IrisFeaturesList()
    iris_features_list.iris_features_list.append(IrisFeatures(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
    iris_features_list.iris_features_list.append(IrisFeatures(sepal_length=6.1, sepal_width=4.5, petal_length=2.4, petal_width=1.2))
    return iris_features_list

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_mock_data(producer, topic, iris_features_list):
    logger.info(f"Sending mock data to topic: {topic}")
    producer.produce(topic=topic, 
                     value=iris_features_list.SerializeToString(),
                     key=None,
                     on_delivery=delivery_report)
    producer.flush()


def main():
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    # topics = os.environ.get('KAFKA_TOPICS', 'topic1,topic2,topic3').split(',')
    topic = os.environ.get("KAFKA_MOCK_DATA_TOPIC")

    time.sleep(10)

    logger.info(f"Starting mock data generator with broker: {broker}, group: {group}, topic: {topic}")
       
    producer_config = {
        'bootstrap.servers': broker,
#        'group.id': group,
#        'auto.offset.reset': 'earliest',
        'acks': 'all',
        'broker.address.family': 'v4',  # Enforce IPv4 connections
        'retries': 3,  # Set the maximum number of retries
        'retry.backoff.ms': 100, # Optional: Time to wait before retrying (in milliseconds)
    }
    producer = Producer(producer_config)

    iris_features_list = generate_mock_data()
    logger.info(f"iris_features_list: {iris_features_list}")
    logger.info(f"iris_features_list.SerializeToString(): {iris_features_list.SerializeToString()}")
    
    try:
        while True:
            send_mock_data(producer, topic, iris_features_list)
            time.sleep(1)
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")
    finally:
        producer.flush()

    logger.info("Mock data generator finished")


if __name__ == "__main__":
    main()
    