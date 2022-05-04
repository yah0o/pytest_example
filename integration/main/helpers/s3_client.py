import boto3.session
from botocore.exceptions import ClientError

from integration.main.logger import log


class S3Client(object):

    def __init__(self, access_key=None, secret_key=None,
                 endpoint_url=None, region=None):
        """
        If access_key and secret_key are not specified boto3 will get
        them from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment
        variables.
        If endpoint_url is not specified boto3 will use default AWS 
        endpoint url.
        If region is not specified boto3 will use defailt regions
        for AWS account.

        :param access_key:
        :param secret_key:
        :param endpoint_url:
        :param region:
        """
        if endpoint_url and endpoint_url.startswith("http://"):
            use_ssl = False
        else:
            use_ssl = True

        self.session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        self.client = self.session.client(
            's3', endpoint_url=endpoint_url, use_ssl=use_ssl)
        self.resource = self.session.resource(
            's3', endpoint_url=endpoint_url, use_ssl=use_ssl)

    def upload(self, filename, bucket, key):
        """
        :param filename:
        :param bucket:
        :param key:
        """
        try:
            with open(filename, 'rb') as data:
                self.client.upload_fileobj(data, bucket, key)
                log.info("Uploaded: {} to Bucket: {}".format(key, bucket))
        except ClientError as e:
            log.error("Unexpected error: %s" % e.response['Error']['Code'])

    def download(self, bucket, filename, key):
        """
        :param bucket:
        :param filename:
        :param key:
        """
        try:
            self.client.download_file(bucket, filename, key)
            log.info("Downloaded: %s" % key)
        except ClientError as e:
            log.error("Unexpected error: %s" % e.response['Error']['Code'])

    def delete(self, bucket, key):
        """
        :param bucket:
        :param key:
        """
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            log.info("Deleted: {} from Bucket: {}".format(key, bucket))
        except ClientError as e:
            log.error("Unexpected error: %s" % e.response['Error']['Code'])

    def get_object(self, bucket, key):
        """
        :param bucket:
        :param key:
        :return S3 object:
        """
        s3_object = None
        try:
            s3_object = self.resource.Object(bucket, key)
            import json
            print(s3_object)
        except ClientError as e:
            log.error("Unexpected error: %s" % e.response['Error']['Code'])
        return s3_object

    def list_keys_in_bucket(self, bucket, prefix=None):
        """
        :param bucket:
        :param prefix:
        :return keys:
        """
        keys = []
        try:
            if prefix is None:
                resp = self.client.list_objects_v2(Bucket=bucket)
            else:
                resp = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
                import json
                print(json.dumps(resp['Prefix'], indent=2))

            keys.append(resp['Prefix'])
            for key in keys:
                log.info("Key: %s" % key)
        except ClientError as e:
            log.error("Unexpected error: %s" % e.response['Error']['Code'])
        return keys

    def list_buckets(self):
        """
        :return buckets:
        """
        buckets = []
        try:
            response = self.client.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            for bucket in buckets:
                log.info("Bucket: %s" % bucket)
        except ClientError as e:
            log.error("Unexpected error: %s" % e.response['Error']['Code'])
        return buckets
