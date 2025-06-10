import os
import json
# TODO: remove logging
import logging
from loguru import logger
from pprint import pformat
from ingester import Ingester

def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    logger.info(f"KAFKA Stats: {pformat(stats_json)}")

def main():
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    stats_interval_ms = os.environ.get("KAFKA_STATS_INTERVAL_MS")
    topic_from = os.environ.get("KAFKA_TOPIC_INGESTOR_FROM")
    topic_to = os.environ.get("KAFKA_TOPIC_INGESTOR_TO")
    
    # Split the string into a list of topics
    topics_list = [topic.strip() for topic in topic_from.split(',')] if topic_from else []

    if logger.level == logging.DEBUG:
        ingester = Ingester(broker, group, topic_from, topic_to, topics_list, stats_interval_ms, stats_cb)
    else:
        ingester = Ingester(broker, group, topic_from, topic_to, topics_list, stats_interval_ms, None)
    
    try:
        logger.info("Starting ingester")
        ingester.run()
        logger.info("Ingester completed")
    except Exception as e:
        logger.error(f"Error running ingester: {e}")
    finally:
        ingester.close()

if __name__ == "__main__":
    main()
