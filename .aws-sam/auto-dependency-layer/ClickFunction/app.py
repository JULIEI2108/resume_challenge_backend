import json
import boto3
import os

# import requests
table_name = os.environ['TABLENAME']

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response['Items']
    if len(items) == 0 :
        item = {
             "clickNumber" : 1,
             "resumevisit" : 1,
        }
        table.put_item(Item=item)
        resumeVisit = 1
    else:
        resumeVisit=items[0]['resumevisit']
        key = {'clickNumber': 1}
        resumeVisit += 1
        update_expression = 'SET resumevisit= :val1'
        expression_attribute_values = {':val1': resumeVisit}

        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "Click Number": str(resumeVisit),
        }),
    }
