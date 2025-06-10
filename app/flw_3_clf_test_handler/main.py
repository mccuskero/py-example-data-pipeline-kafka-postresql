import os
import logging
from loguru import logger
from classifier import Classifier

def main():
    logger.info("starting flw-3-clf-test-handler")

    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    topic_from = os.environ.get("KAFKA_TOPIC_CLASSIFIER_FROM")
    topic_to = os.environ.get("KAFKA_TOPIC_CLASSIFIER_TO")
    stats_interval_ms = os.environ.get("KAFKA_STATS_INTERVAL_MS")
    stats_cb = os.environ.get("KAFKA_STATS_CB")

    # Split the string into a list of topics
    topics_list = [topic.strip() for topic in topic_from.split(',')] if topic_from else []

    if logger.level == logging.DEBUG:
        classifier = Classifier(broker, group, topic_from, topic_to, topics_list, stats_interval_ms, stats_cb)
    else:
        classifier = Classifier(broker, group, topic_from, topic_to, topics_list, stats_interval_ms, None)
        
    try:    
        classifier.run()
    except Exception as e:
        logger.error(f"Error running classifier: {e}")
    finally:
        classifier.close()
    
if __name__ == "__main__":
    main()
