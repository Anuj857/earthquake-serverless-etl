import json
import os
import urllib.request
from datetime import datetime

import boto3

# Create S3 client
s3 = boto3.client("s3")


def lambda_handler(event, context):
    try:
        # Read environment variables
        bucket_name = os.environ["S3_BUCKET"]
        raw_prefix = os.environ["RAW_PREFIX"]
        usgs_url = os.environ["USGS_URL"]

        print("Fetch Lambda Started")

        # Call USGS API
        response = urllib.request.urlopen(usgs_url)

        if response.status != 200:
            raise Exception(f"Failed to fetch data. HTTP Status: {response.status}")

        # Read API response
        data = json.loads(response.read().decode("utf-8"))

        # Create timestamped filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_name = f"{raw_prefix}earthquake_{timestamp}.json"

        # Upload JSON to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data),
            ContentType="application/json"
        )

        print(f"Successfully uploaded: {file_name}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Earthquake data uploaded successfully.",
                    "file": file_name
                }
            )
        }

    except Exception as e:
        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": str(e)
                }
            )
        }