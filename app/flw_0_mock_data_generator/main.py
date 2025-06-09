import sys
import os
import time
import signal
from loguru import logger

# Get the absolute path to the src directory
# need to ".." to go up one level to get to the root directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
# Insert the src directory at the beginning of sys.path
sys.path.insert(0, src_path)
# print(sys.path)

from mock_data_generator import MockDataGenerator

def handle_signals(signum, frame):
    logger.info(f"Signal {signum} received. Exiting...")
    sys.exit(0)
    
signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)


def main():
    broker = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    group = os.environ.get("KAFKA_GROUP_ID")
    topic_to = os.environ.get("KAFKA_TOPIC_MOCK_DATA_GENERATOR_TO")

    # TODO: remove this... ??
    time.sleep(10)

    logger.info(f"Starting mock data generator with broker: {broker}, group: {group}, topic: {topic_to}")
    
    mock_data_generator = MockDataGenerator(broker, topic_to)
    try:
        mock_data_generator.generate()
    except Exception as e:
        logger.error(f"Error generating mock data: {e}")
    finally:
        mock_data_generator.close()
    
if __name__ == "__main__":
    main()
    