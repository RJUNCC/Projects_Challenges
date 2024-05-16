# from quixstreams import Application
import os
from datetime import timedelta
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9094')

# example sending a message
producer.send('trading_topic', b'Hello, World!')

producer.flush()