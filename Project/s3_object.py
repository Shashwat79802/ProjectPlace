import boto3
from django.conf import settings


client = boto3.client('s3')

def object_remover(object: str):
   response = client.delete_object(
                            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                            Key=object,
                            ExpectedBucketOwner=settings.AWS_BUCKET_OWNER_ID
                        )
