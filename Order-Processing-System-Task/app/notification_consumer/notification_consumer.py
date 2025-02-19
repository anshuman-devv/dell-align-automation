import pika
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import (
    EMAIL_PASSWORD, EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PORT, RABBITMQ_HOST, RABBITMQ_QUEUE_NOTIFICATIONS)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class NotificationConsumer:

    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=RABBITMQ_QUEUE_NOTIFICATIONS, durable=True)
            self.channel.basic_qos(prefetch_count=1)

        except Exception as e:
            logging.error(f"Failed to initialize RabbitMQ connection: {e}")
            sys.exit(1)

    def send_email(self, to_email: str, subject: str, body: str) -> None:
        print(f"🔹 Sending email to: {to_email}")
        try:
            message = MIMEMultipart()
            message["From"] = EMAIL_ADDRESS
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())
                print("✅ Email sent successfully!")

            logging.info(f"Email sent successfully to {to_email}")
        except smtplib.SMTPException as e:
            logging.error(f"Failed to send email to {to_email}: {e}")

    def process_message(self, ch, method, properties, body) -> None:
        try:
            order_info = json.loads(body)
            order_id = order_info.get("order_id")
            customer_email = order_info.get("email")
            customer_name = order_info.get("customer_name")
            product = order_info.get("product")
            quantity = order_info.get("quantity")

            if customer_email:
                subject = f"Order Confirmation - #{order_id}"
                body = (
                    f"Hi {customer_name},\n\n"
                    f"Thank you for your order.\n"
                    f"Product: {product}\n"
                    f"Quantity: {quantity}\n"
                    f"Your order is being processed.\n\n"
                    f"Best regards,\nOrder Processing Team"
                )
                self.send_email(customer_email, subject, body)
            else:
                logging.warning(f"No email provided for Order #{order_id}.")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        except json.JSONDecodeError:
            logging.error("Error decoding JSON message. Skipping...")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logging.error(f"Error processing notification: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        try:
            self.channel.basic_consume(
                queue=RABBITMQ_QUEUE_NOTIFICATIONS,
                on_message_callback=self.process_message
            )
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logging.info("Shutting down gracefully...")
        except Exception as e:
            logging.error(f"Consumer encountered an error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            if self.connection:
                self.connection.close()
                logging.info("RabbitMQ connection closed.")
        except Exception as e:
            logging.error(f"Error closing RabbitMQ connection: {e}")


if __name__ == "__main__":
    consumer = NotificationConsumer()
    consumer.start_consuming()