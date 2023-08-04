import boto3
import json
import psycopg2

# AWS SQS Queue details
sqs_queue_url = 'http://localhost:4566/000000000000/login-queue`'
region_name = 'us-west-2'

# PostgreSQL database details
db_host = 'localhost'
db_port = '5432'
db_user = 'postgres'
db_password = 'postgres'

# Masking function for device_id and ip
def mask_field(field_value):
    # Replace first 3 characters with pound signs for data analysts to understand
    return '###' + field_value[3:]

# Function to process the SQS messages and store data in PostgreSQL
def process_messages():
    try:
        # Connect to SQS Queue
        sqs = boto3.client('sqs', region_name=region_name)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )
        cur = conn.cursor()

        # Receive and process messages from SQS Queue
        response = sqs.receive_message(QueueUrl=sqs_queue_url, MaxNumberOfMessages=10)
        messages = response.get('Messages', [])
        while messages:
            for message in messages:
                body = json.loads(message['Body'])
                # Extract data from the SQS message (assuming JSON data in 'data' key)
                data = json.loads(body['data'])

                # Mask device_id and ip fields
                data['device_id'] = mask_field(data['device_id'])
                data['ip'] = mask_field(data['ip'])

                # Store the processed data into PostgreSQL database
                cur.execute(
                    "INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (data['user_id'], data['device_type'], data['ip'], data['device_id'], data['locale'], data['app_version'], data['create_date'])
                )
                conn.commit()

                # Delete the processed message from SQS Queue
                sqs.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=message['ReceiptHandle'])

            # Continue fetching messages until none are left in the queue
            response = sqs.receive_message(QueueUrl=sqs_queue_url, MaxNumberOfMessages=10)
            messages = response.get('Messages', [])

        # Close the database connection
        cur.close()
        conn.close()

        print("Processing completed successfully.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    process_messages()
