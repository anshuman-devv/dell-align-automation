import mock
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from notification_consumer.notification_consumer import NotificationConsumer

def test_process_message(mock_dependencies, sample_order):
    consumer = NotificationConsumer()
    
    mock_channel = mock_dependencies["rabbitmq"].channel()
    mock_smtp_instance = mock_dependencies["email_instance"]
    body = json.dumps(sample_order)

    consumer.process_message(mock_channel, mock.Mock(), mock.Mock(), body)

    mock_channel.basic_ack.assert_called_once()
    mock_smtp_instance.sendmail.assert_called_once()