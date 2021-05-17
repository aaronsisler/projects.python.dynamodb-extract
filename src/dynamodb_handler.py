import json
import boto3
import botocore


def main(event, context):
    data = None
    s3_bucket_name = "eandb-dynamodb-extract"
    client = boto3.client('dynamodb')

    try:
        response = client.export_table_to_point_in_time(
            TableArn="arn:aws:dynamodb:us-east-1:654918520080:table/JAVA_MAPPER_TEST",
            S3Bucket=s3_bucket_name,
            ExportFormat='DYNAMODB_JSON'
        )
        print(response)
        export_arn = response['ExportDescription']['ExportArn']
        export_folder_name = export_arn.partition("/export/")[2]
        print(export_folder_name)
        print("Completed Export")
        data = {
            "export_folder_name": f'AWSDynamoDB/{export_folder_name}/data',
            "s3_bucket_name": s3_bucket_name
        }
    except botocore.exceptions.ClientError as e:
        print(e)
        print("Failed")
        data = "Export failed"

    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response
