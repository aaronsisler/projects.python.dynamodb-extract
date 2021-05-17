import json
import boto3
import botocore
import gzip
from io import BytesIO
from datetime import datetime
import time


def main(event, context):
    print(event)

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H:%M:%S")
    s3_unzipped_file_key = dt_string + ".json"

    s3_bucket_name = "eandb-dynamodb-extract"
    s3_gzipped_file_key = event["Records"][0]["s3"]["object"]["key"]

    print(f"s3 Object Key name: {s3_gzipped_file_key}")

    try:
        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(  # upload a new obj to s3
            Fileobj=gzip.GzipFile(  # read in the output of gzip -d
                None,  # just return output as BytesIO
                'rb',  # read binary
                fileobj=BytesIO(s3_client.get_object(Bucket=s3_bucket_name, Key=s3_gzipped_file_key)['Body'].read())),
            Bucket=s3_bucket_name,  # target bucket, writing to
            Key=s3_unzipped_file_key)  # target key, writing to
    except botocore.exceptions.ClientError as e:
        print("Failed")