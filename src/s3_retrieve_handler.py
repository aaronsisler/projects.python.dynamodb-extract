import json
import boto3
import botocore
import gzip
from io import BytesIO
from datetime import datetime
import time


def main(event, context):
    raw_body = event['body']
    body = json.loads(raw_body)
    data = None
    s3_gzipped_file_key = None

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H:%M:%S")
    s3_unzipped_file_key = dt_string + ".json"

    if 'export_folder_name' not in body or 's3_bucket_name' not in body:
        return {
            "statusCode": 400,
            "body": json.dumps('Please provide 2 values to add')
        }

    export_folder_name = body['export_folder_name']
    s3_bucket_name = body['s3_bucket_name']

    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')  # optional

    continue_polling = True
    max_number_of_iterations = 12
    current_iteration = 1
    print("Starting while loop")
    while continue_polling or current_iteration < max_number_of_iterations:
        try:
            print("About to try")
            bucket = s3_resource.Bucket(s3_bucket_name)
            bucket_objects = bucket.objects.filter(Prefix=export_folder_name)
            print("We have tried")
            if len(list(bucket_objects.limit(1))) == 0:
                print("No items found. Sleeping 5 seconds")
                time.sleep(5)
                continue

            print("About to loop through for")
            for obj in bucket_objects:
                print(obj)
                if obj.key.endswith("json.gz"):
                    s3_gzipped_file_key = obj.key
                    continue_polling = False
                    break

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
                data = "Failed"
            else:
                print("Failed")
                data = "Failed"
        finally:
            current_iteration = current_iteration + 1
            print(f'Current Iteration: {current_iteration}')

    print("After while loop")
    if continue_polling is False:
        try:
            s3_client.upload_fileobj(  # upload a new obj to s3
                Fileobj=gzip.GzipFile(  # read in the output of gzip -d
                    None,  # just return output as BytesIO
                    'rb',  # read binary
                    fileobj=BytesIO(s3_client.get_object(Bucket=s3_bucket_name, Key=s3_gzipped_file_key)['Body'].read())),
                Bucket=s3_bucket_name,  # target bucket, writing to
                Key=s3_unzipped_file_key)  # target key, writing to
            data = "Worked"
        except botocore.exceptions.ClientError as e:
            print("Failed")
            data = "Failed"

    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response
