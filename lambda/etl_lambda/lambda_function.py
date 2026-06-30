import json
import os
import boto3

# AWS Clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment Variable
table_name = os.environ["DYNAMODB_TABLE"]
table = dynamodb.Table(table_name)


def get_severity(magnitude):
    """
    Return earthquake severity based on magnitude.
    """
    if magnitude is None:
        return "Unknown"

    if magnitude < 2.5:
        return "Minor"
    elif magnitude < 5.5:
        return "Moderate"
    elif magnitude < 7.0:
        return "Strong"
    else:
        return "Major"


def lambda_handler(event, context):

    print("========== ETL Lambda Started ==========")

    try:

        # -------------------------
        # Extract bucket and object
        # -------------------------

        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]

        print(f"Bucket : {bucket_name}")
        print(f"Object : {object_key}")

        # -------------------------
        # Download file from S3
        # -------------------------

        response = s3.get_object(
            Bucket=bucket_name,
            Key=object_key
        )

        data = json.loads(
            response["Body"].read().decode("utf-8")
        )

        print("JSON downloaded successfully")

        features = data.get("features", [])

        print(f"Total Earthquakes Found : {len(features)}")

        inserted = 0
        rejected = 0

        # -------------------------
        # Transform & Load
        # -------------------------

        for feature in features:

            try:

                properties = feature.get("properties", {})
                geometry = feature.get("geometry", {})

                record_id = feature.get("id")

                magnitude = properties.get("mag")
                place = properties.get("place")
                event_time = properties.get("time")

                coordinates = geometry.get("coordinates", [])

                longitude = coordinates[0] if len(coordinates) > 0 else None
                latitude = coordinates[1] if len(coordinates) > 1 else None
                depth = coordinates[2] if len(coordinates) > 2 else None

                # Skip invalid records

                if record_id is None or magnitude is None:
                    rejected += 1
                    continue

                severity = get_severity(magnitude)

                item = {
                    "record_id": record_id,
                    "magnitude": str(magnitude),
                    "place": place,
                    "time": str(event_time),
                    "latitude": str(latitude),
                    "longitude": str(longitude),
                    "depth": str(depth),
                    "severity": severity
                }

                table.put_item(Item=item)

                inserted += 1

            except Exception as e:

                print(f"Record Error : {e}")
                rejected += 1

        print("========== ETL SUMMARY ==========")
        print(f"Inserted : {inserted}")
        print(f"Rejected : {rejected}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "Inserted": inserted,
                "Rejected": rejected
            })
        }

    except Exception as e:

        print(f"Fatal Error : {e}")

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }
    
    