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
    table_arn = "arn:aws:dynamodb:us-east-1:654918520080:table/JAVA_MAPPER_TEST"
    bucket_name = "eandb-dynamodb-extract"

    try:
        response = client.export_table_to_point_in_time(
            TableArn=table_arn,
            S3Bucket=bucket_name,
            ExportFormat='DYNAMODB_JSON'
        )
        print("Completed Export")
        data = "Export Success"
    except botocore.exceptions.ClientError as e:
        print("Failed")
        data = "Export failed"

    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response
