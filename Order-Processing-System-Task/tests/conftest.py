import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_dependencies():
    with patch("redis.StrictRedis") as mock_redis, \
         patch("pika.BlockingConnection") as mock_rabbitmq, \
         patch("smtplib.SMTP_SSL") as mock_email:

        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        mock_rabbitmq_instance = MagicMock()
        mock_rabbitmq.return_value = mock_rabbitmq_instance

        mock_smtp_instance = mock_email.return_value
        mock_smtp_instance.login.return_value = None
        mock_smtp_instance.sendmail.return_value = None

        yield {
            "email_instance": mock_smtp_instance, 
            "redis": mock_redis_instance,
            "rabbitmq": mock_rabbitmq_instance,
            "email": mock_email
        }

@pytest.fixture
def sample_order():
    return {
        "order_id": "12345",
        "customer_name": "Test User",
        "email": "test@gmail.com",
        "product": "Laptop",
        "quantity": 1,
        "status": "New"
    }
