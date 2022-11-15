import boto3

s3 = boto3.resource(
    's3',
    aws_access_key_id='ROOTUSER',
    aws_secret_access_key='CHANGEME123',
    endpoint_url='http://localhost:9000',
    use_ssl=False
)


def get_object_bytes(bucket: str, key: str) -> bytes:
    obj = s3.Object(bucket, key)
    return obj.get()['Body'].read()
