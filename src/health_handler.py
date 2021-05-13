import json


def main(event, context):

    response = {
        "statusCode": 200,
        "body": json.dumps('Service is alive and well')
    }

    return response
