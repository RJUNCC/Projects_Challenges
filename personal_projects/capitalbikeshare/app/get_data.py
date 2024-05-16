import boto3
import logging
import pandas as pd
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import pyarrow.parquet as pq

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create Kafka producer configuration
# conf = {
#     'bootstrap.servers': 'localhost:9092',
# }

# # Create Kafka producer instance
# producer = Producer(conf)

# # Define delivery callback function
# def delivery_report(err, msg):
#     if err is not None:
#         print(f'Message delivery failed: {err}')
#     else:
#         print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# # Initialize S3 client
# s3 = boto3.client('s3')

# # S3 bucket and prefix
# bucket_name = 'capitalbikesharegbfs'
# prefix = 'parquet_'

# # List objects in S3 bucket with specified prefix
# response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# # Iterate over objects in the S3 bucket
# for obj in response.get('Contents', []):
#     # Get object key (file name)
#     object_key = obj['Key']
    
#     # Download Parquet file from S3
#     response = s3.get_object(Bucket=bucket_name, Key=object_key)
#     parquet_data = response['Body'].read()
    
#     # Publish message to Kafka topic
#     producer.produce('parquet_files_topic', key=object_key.encode('utf-8'), value=parquet_data, callback=delivery_report)

# # Wait for all messages to be delivered
# producer.flush()

# # Close Kafka producer
# producer.close()

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'parquet_consumer_group',
    'auto.offset.reset': 'earliest'
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to Kafka topic containing Parquet file data
consumer.subscribe(['system_information_parquet_data_topic'])

# Initialize empty DataFrame to store Parquet file data
parquet_df = pd.DataFrame()

try:
    while True:
        # Poll for messages from Kafka
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            # Handle errors
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition
                continue
            else:
                # Handle other errors
                raise KafkaException(msg.error())
        else:
            # Deserialize message value (Parquet file data)
            parquet_data = msg.value()
            
            # Read Parquet data into DataFrame
            df = pd.read_parquet(parquet_data)
            
            # Append DataFrame to the main DataFrame
            parquet_df = parquet_df.append(df, ignore_index=True)
            
finally:
    # Close Kafka consumer
    consumer.close()

# print(parquet_df.head())