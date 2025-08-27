import os
import json
import logging
from kafka import KafkaProducer, KafkaConsumer
from threading import Lock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaConnection:
    _producer_instance = None
    _consumer_instances = {}
    _lock = Lock()

    @classmethod
    def get_producer(cls):
        with cls._lock:
            if cls._producer_instance is None:
                try:
                    cls._producer_instance = KafkaProducer(
                        bootstrap_servers=f"{os.environ['KAFKA_SERVER']}:{os.environ['KAFKA_PORT']}",
                        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                        retries=5,
                    )
                    logger.info("Kafka Producer initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to initialize Kafka Producer: {str(e)}")
                    cls._producer_instance = None
            return cls._producer_instance

    @classmethod
    def get_consumer(
        cls, topic, group_id=None, enable_auto_commit=True, auto_offset_reset="earliest"
    ):
        key = (topic, group_id)
        with cls._lock:
            if key not in cls._consumer_instances:
                try:
                    consumer = KafkaConsumer(
                        topic,
                        group_id=os.environ["KAFKA_GROUP_ID"],
                        bootstrap_servers=f"{os.environ['KAFKA_SERVER']}:{os.environ['KAFKA_PORT']}",
                        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                        enable_auto_commit=enable_auto_commit,
                        auto_offset_reset=auto_offset_reset,
                        consumer_timeout_ms=10000,
                        max_poll_records=100,
                        max_poll_interval_ms=600000,
                    )
                    cls._consumer_instances[key] = consumer
                    logger.info(
                        f"Kafka Consumer initialized for topic '{topic}' and group_id '{group_id}'."
                    )
                except Exception as e:
                    logger.error(f"Failed to initialize Kafka Consumer: {str(e)}")
                    cls._consumer_instances[key] = None
            return cls._consumer_instances.get(key)

    @classmethod
    def close_all(cls):
        if cls._producer_instance:
            try:
                cls._producer_instance.close()
                logger.info("Kafka Producer closed successfully.")
            except Exception as e:
                logger.error(f"Error closing Kafka Producer: {str(e)}")
        for (topic, group_id), consumer in cls._consumer_instances.items():
            if consumer:
                try:
                    consumer.close()
                    logger.info(
                        f"Kafka Consumer for topic '{topic}' closed successfully."
                    )
                except Exception as e:
                    logger.error(
                        f"Error closing Kafka Consumer for topic '{topic}': {str(e)}"
                    )


"""
# Kirim
KafkaConnection.get_producer().send("my_topic", {"event": "test", "payload": 123})

# Terima
consumer = KafkaConnection.get_consumer("my_topic")
for msg in consumer:
    print("Received:", msg.value)  # Output: {'event': 'test', 'payload': 123}
"""
