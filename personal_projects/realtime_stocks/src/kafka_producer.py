from confluent_kafka import Producer
import socket
import dotenv
import load_data
from load_data import load_json_file
import os
import json

dotenv.load_dotenv('../.env')
# Producer sends data as messages to Kafka cluster or topic
# Consumer or consumer group reads data from kafka topic or cluster and writes it to data server
# Kafka cluster has mulitple topics. Those topics have partitions. Those partitions are topic fractions and they are stored in different nodes of the local system.
# The partition takes a topic log and breaks it into multiple logs.
# Kafka cluster can be divided into let's say 600 partitions, so each consumer in the consumer group might take 100 paritions if there's 6 consumers. 
def send_data_to_kafka(kafka_topic):
    config = {
        'bootstrap.servers':'host1:9092, host2:9092, pkc-p11xm.us-east-1.aws.confluent.cloud:9092',
        'security.protocol':'SASL_SSL',
        'sasl.mechanism':'PLAIN',
        'sasl.username':os.getenv('KAFKA_API_KEY'),
        'sasl.password':os.getenv('KAFKA_API_SECRET'),
        'client.id':socket.gethostname()
    }

    producer = Producer(config)

    def delivery_report(err, msg):
        if err is  not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()}[{msg.partition()}]")

    # serialize json data
    json_str = json.dumps(load_data.DATA_DIR + "stock_data.json")

    # encode json string to bytes
    json_bytes = json_str.encode('utf-8')

    # send data to Kafka topic
    producer.produce(kafka_topic, value=json_bytes, callback=delivery_report)

    # wait for message deliveries
    producer.flush()

send_data_to_kafka("stock-data")


