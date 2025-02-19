import pika
import json
import uuid
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import RABBITMQ_HOST, RABBITMQ_QUEUE_ORDERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class OrderProducer:

    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=RABBITMQ_QUEUE_ORDERS, durable=True)

        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            sys.exit(1)

    def send_order(self, order_data: dict) -> None:
        try:
            order_json = json.dumps(order_data)

            self.channel.basic_publish(
                exchange="",
                routing_key=RABBITMQ_QUEUE_ORDERS,
                body=order_json,
                properties=pika.BasicProperties(delivery_mode=2)
            )

            logging.info(f"Order sent successfully: {order_json}")
        except Exception as e:
            logging.error(f"Failed to send order: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            logging.error(f"Error closing RabbitMQ connection: {e}")


if __name__ == "__main__":
    order = {
        "order_id": str(uuid.uuid4()),
        "customer_name": "Anshuman Pandey",
        "email": "xyz@gmail.com",
        "product": "Laptop",
        "quantity": 1,
        "status": "New"
    }

    producer = OrderProducer()
    producer.send_order(order)
