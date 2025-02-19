import pika
import json
import logging
import redis
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import RABBITMQ_HOST, RABBITMQ_QUEUE_ORDERS, RABBITMQ_QUEUE_NOTIFICATIONS, REDIS_HOST, REDIS_PORT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class OrderConsumer:
            
    def __init__(self, redis_client=None):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            self.channel = self.connection.channel()

            self.redis_client = redis_client or redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

            self.channel.queue_declare(queue=RABBITMQ_QUEUE_ORDERS, durable=True)
            self.channel.queue_declare(queue=RABBITMQ_QUEUE_NOTIFICATIONS, durable=True)

        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            sys.exit(1)

    def process_order(self, ch, method, body):
        order_data = json.loads(body)
        try:
            print(f"🔹 Saving to Redis: {order_data}")
            self.redis_client.set(f"Order:{order_data['order_id']}", json.dumps(order_data)) 
                
            logging.info(f"Order {order_data['order_id']} stored in Redis successfully.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Error storing order {order_data['order_id']} in Redis: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def publish_notification(self, order_info):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()

            channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE_NOTIFICATIONS,
                body=json.dumps(order_info),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logging.info(f"Order {order_info['order_id']} sent to notifications queue.")
            connection.close()
        except Exception as e:
            logging.error(f"Error sending to notifications queue: {e}")

    def callback(self, ch, method, properties, body):
        try:
            order_info = json.loads(body)
            self.process_order(ch, method, body)        
            self.publish_notification(order_info)  
        except Exception as e:
            logging.error(f"Error processing order: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def consume_orders(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=RABBITMQ_QUEUE_ORDERS, on_message_callback=self.callback)
        logging.info("Order Consumer is waiting for orders...")
        self.channel.start_consuming()

    def cleanup(self):
        try:
            if self.connection:
                self.connection.close()
                logging.info("RabbitMQ connection closed.")
        except Exception as e:  
            logging.error(f"Error closing RabbitMQ connection: {e}")


if __name__ == "__main__":
    consumer = OrderConsumer()
    try:
        consumer.consume_orders()
    except KeyboardInterrupt:
        logging.info("Terminating Order Consumer...")
    finally:
        consumer.cleanup()