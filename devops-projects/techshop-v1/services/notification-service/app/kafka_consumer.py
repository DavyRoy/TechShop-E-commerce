import os
import json
import time
import signal
import sys
from app.handlers import on_order_created, on_order_updated, on_order_cancelled

KAFKA_BROKER   = os.getenv('KAFKA_BROKER', 'localhost:9092')
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP', 'notification-service-group')
MAX_RETRIES    = 3

HANDLERS = {
    'order.created':   on_order_created,
    'order.updated':   on_order_updated,
    'order.cancelled': on_order_cancelled,
}

def handle_message(message):
    handler = HANDLERS.get(message.topic)
    if not handler:
        print(f"No handler for topic: {message.topic}")
        return

    for attempt in range(MAX_RETRIES):
        try:
            handler(message.value)
            break
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                print(f"Failed after {MAX_RETRIES} attempts: {e}")
            else:
                time.sleep(1)

def start_consumer():
    while True:
        try:
            from kafka import KafkaConsumer
            consumer = KafkaConsumer(
                'order.created', 'order.updated', 'order.cancelled',
                bootstrap_servers=[KAFKA_BROKER],
                group_id=CONSUMER_GROUP,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest'
            )
            break
        except Exception as e:
            print(f"Kafka unavailable: {e}, retrying in 5s...")
            time.sleep(5)

    def shutdown(sig, frame):
        print("Shutting down gracefully...")
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print("Notification Service started, waiting for events...")

    for message in consumer:
        print(f"Received event: {message.topic}")
        handle_message(message)