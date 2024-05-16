import logging
from kafka import KafkaProducer

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Example message production
try:
    for i in range(10):
        producer.send('test_topic', value=f'Message {i}'.encode('utf-8'))
        logging.info(f"Message {i} sent successfully")
except Exception as e:
    logging.error(f"Error sending message: {e}")
finally:
    producer.close()

