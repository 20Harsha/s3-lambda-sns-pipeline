import json
import boto3
import pandas as pd
import io
import logging
from datetime import date

# Initialize AWS clients
s3 = boto3.client("s3")
sns = boto3.client("sns")

# SNS Topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:388893392277:File_Processing_Updates"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def lambda_handler(event, context):
    try:
        logger.info("Function execution started")
        logger.info(f"Event received: {event}")

        event_time = event["Records"][0]["eventTime"]
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_name = event["Records"][0]["s3"]["object"]["key"]
        print(file_name)
        logger.info(f"Event happened at: {event_time}")
        logger.info(f"File uploaded in bucket: {bucket_name}")
        logger.info(f"Filename: {file_name}")

        # Extract filename parts
        filename = file_name.split('/')
        filename_split = filename[1].split("-")
        file_date = pd.to_datetime(
                filename_split[0] + "-" + filename_split[1] + "-" + filename_split[2]
        ).date()

        b1 = filename_split[3].split(".")
        base_name = b1[0]
        file_format = b1[1]

        logger.info(f"Extracted File Date: {file_date}")
        logger.info(f"Base Name: {base_name}, Format: {file_format}")

        # Validate file format and structure
        if isinstance(file_date, date) and base_name == "raw_input" and file_format == "json":
            # Read file from S3
            file = s3.get_object(Bucket=bucket_name, Key=file_name)
            df = pd.read_json(file["Body"])

            # Filter required data
            target_file = df[df["status"] == "delivered"]
            new_file_name = f"{file_date}_processed_file.json"

            # Use memory buffer instead of writing to disk
            buffer = io.BytesIO()
            target_file.to_json(buffer, orient="records")
            buffer.seek(0)

            # Upload processed file to S3
            s3.put_object(
                Bucket=bucket_name,
                Key=f"doordash-target-zn/{new_file_name}",
                Body=buffer.getvalue(),
            )

            # Send SNS Notification
            sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="File Processing Successful",
                    Message=f"File '{file_name}' has been processed successfully and saved as 'doordash-target-zn/{new_file_name}'",
            )

            logger.info(f"Successfully processed and uploaded: doordash-target-zn/{new_file_name}")

        else:
            logger.warning("Uploaded file is not in the correct format.")

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)

        # Send failure notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="File Processing Failed",
            Message=f"Processing of file '{file_name}' has failed due to: {str(e)}",
        )
