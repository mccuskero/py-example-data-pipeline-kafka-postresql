import os
import sys
import logging

from loguru import logger
from postprocessor import Postprocessor

def main():
    logger.info("starting flw-4-postprocessor")
    
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    topic_from = os.environ.get("KAFKA_TOPIC_POSTPROCESSOR_FROM")
    stats_interval_ms = os.environ.get("KAFKA_STATS_INTERVAL_MS")
    stats_cb = os.environ.get("KAFKA_STATS_CB")
    
    # Split the string into a list of topics
    topics_list = [topic.strip() for topic in topic_from.split(',')] if topic_from else []
    
    if logger.level == logging.DEBUG:
        postprocessor = Postprocessor(broker, group, topic_from, None, topics_list, stats_interval_ms, stats_cb)
    else:
        postprocessor = Postprocessor(broker, group, topic_from, None, topics_list, stats_interval_ms, None)
        
    try:
        postprocessor.run()
    except Exception as e:
        logger.error(f"Error running postprocessor: {e}")
    finally:
        postprocessor.close()
            
if __name__ == "__main__":
    main()
