import os
from loguru import logger

from confluent_kafka import Producer

class MsgProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        
        self.producer_config = {
            'bootstrap.servers': broker,
            'acks': 'all',
            'broker.address.family': 'v4',  # Enforce IPv4 connections
            'retries': 3,  # Set the maximum number of retries
            'retry.backoff.ms': 100, # Optional: Time to wait before retrying (in milliseconds)
        }
        
        self.producer = Producer(self.producer_config)

    def produce(self, serialized_msg):
        logger.info(f"Sending msg to topic: {self.topic}")
        self.producer.produce(self.topic, serialized_msg)
        self.producer.flush()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def __del__(self):
        pass
    
    