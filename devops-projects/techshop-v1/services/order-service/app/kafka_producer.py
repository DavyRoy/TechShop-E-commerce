import os
import json
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')

try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    print(f"Kafka unavailable: {e}")
    producer = None

def _publish(topic: str, data: dict):
    if producer is None:
        print(f"Kafka unavailable, skipping event to {topic}: {data}")
        return
    try:
        producer.send(topic, data)
        producer.flush()
    except Exception as e:
        print(f"Failed to publish to {topic}: {e}")

def publish_order_created(order_data: dict):
    _publish('order.created', order_data)

def publish_order_updated(order_data: dict):
    _publish('order.updated', order_data)

def publish_order_cancelled(order_id: str):
    _publish('order.cancelled', {'order_id': order_id})