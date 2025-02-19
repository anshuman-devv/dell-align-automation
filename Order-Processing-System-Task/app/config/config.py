import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_QUEUE_ORDERS = 'orders'
RABBITMQ_QUEUE_NOTIFICATIONS = 'notifications'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0    

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465    
EMAIL_ADDRESS = "khandelwalakshita041@gmail.com"
EMAIL_PASSWORD = "hgqcutojjnjwovwq"