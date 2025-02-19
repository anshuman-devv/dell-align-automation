import sys
import os
import json
import mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from producers.producers import OrderProducer

def test_send_order(mock_dependencies, sample_order):
    producer = OrderProducer()

    mock_channel = mock_dependencies["rabbitmq"].channel()
    producer.channel = mock_channel

    producer.send_order(sample_order)

    mock_channel.basic_publish.assert_called_once_with(
        exchange="",
        routing_key="orders",
        body=json.dumps(sample_order),
        properties=mock.ANY
    )