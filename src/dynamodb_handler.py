import json
import boto3
import botocore


def recursive_dive(json_dict):
    for key in json_dict:
        print("Key:", key)
        if type(json_dict[key]) == dict:
            recursive_dive(json_dict[key])
        else:
            print("Value:", json_dict[key])


def main(event, context):
    data = None
    client = boto3.client('dynamodb')

    try:
        print("Completed Download")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            print("Failed")

    response = {
        "statusCode": 200,
        "body": json.dumps(data).replace("\n", "")
    }

    return response
