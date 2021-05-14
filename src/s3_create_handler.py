import json
import boto3
import botocore
import os


def recursive_dive(json_dict):
    for key in json_dict:
        print("Key:", key)
        if type(json_dict[key]) == dict:
            recursive_dive(json_dict[key])
        else:
            print("Value:", json_dict[key])


def main(event, context):
    bucket_name = "eandb-dynamodb-extract"
    # dest_filename = "s3-new-file.txt"
    data = None
    raw_body = event['body']
    body = json.loads(raw_body)

    if 'file_contents' not in body or 'dest_filename' not in body:
        return {
            "statusCode": 400,
            "body": json.dumps('Please provide 2 values to add')
        }

    file_contents = body['file_contents']
    dest_filename = body['dest_filename']

    s3 = boto3.resource('s3')

    try:
        upload_object = s3.Object(bucket_name, dest_filename)
        upload_object.put(Body=file_contents)
        data = "It worked"
        print("Completed Upload")
    except botocore.exceptions.ClientError as e:
        print(e)
        print("Failed")
        data = "It failed"

    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response
