import json
import mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from order_consumer.order_consumer import OrderConsumer

def test_process_order(mock_dependencies, sample_order):
    consumer = OrderConsumer()

    mock_channel = mock_dependencies["rabbitmq"].channel()
    consumer.channel = mock_channel

    body = json.dumps(sample_order)
    consumer.process_order(mock_channel, mock.Mock(), body)

    mock_dependencies["redis"].set.assert_called_once_with(f"Order:{sample_order['order_id']}", json.dumps(sample_order))


def test_publish_notification(mock_dependencies, sample_order):
    consumer = OrderConsumer()

    mock_channel = mock_dependencies["rabbitmq"].channel()
    consumer.channel = mock_channel

    consumer.publish_notification(sample_order)

    mock_channel.basic_publish.assert_called_once_with(
        exchange='',
        routing_key="notifications",
        body=json.dumps(sample_order),
        properties=mock.ANY
    )