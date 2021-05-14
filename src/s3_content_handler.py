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
    src_filename = "test-read.json"
    dest_filename = "s3-new-file.json"
    print(os.getcwd())
    data = None

    # with open(os.path.join(os.getcwd(), "dist", filename)) as f:
    #     data = json.load(f)
    #     recursive_dive(data)

    s3 = boto3.resource('s3')

    try:
        bucket = s3.Bucket(bucket_name)
        # Iterates through all the objects, doing the pagination for you. Each obj
        # is an ObjectSummary, so it doesn't contain the body. You'll need to call
        # get to get the whole body.
        for obj in bucket.objects.all():
            key = obj.key
            data = obj.get()['Body'].read().decode("utf-8")
            print(data)
        print("Completed Download")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print("Failed")

    response = {
        "statusCode": 200,
        "body": json.dumps(data).replace("\\n", "")
    }

    return response
