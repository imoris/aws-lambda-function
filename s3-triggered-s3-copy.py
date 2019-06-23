import json
import urllib.parse
import boto3
import re

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    srcBucket = event['Records'][0]['s3']['bucket']['name']
    destBucket = '[YOUR-DESTINATION-BUCKET-NAME]'
    
    srcObj = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    destObj = re.sub(r'[YOUR-SOURCE-DIRECTORY-NAME].','[YOUR-DESTINATION-DIRECTORY-NAME]',srcObj)
    
    print("srcBucket:" + srcBucket)
    print("srcObj:" + srcObj)
    print("destBucket:" + destBucket)
    print("destObj:" + destObj)
    
    try:
        #response = s3.get_object(Bucket=bucket, Key=key)
        response = s3.copy_object(Bucket=destBucket, Key=destObj, CopySource= {'Bucket': srcBucket, 'Key':srcObj}) 
        #print("CONTENT TYPE: " + response['ContentType'])
        return response['ContentType']
        
    except Exception as e:
        print(e)
        print('Error copying object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(srcObj, srcBucket))
        raise e
