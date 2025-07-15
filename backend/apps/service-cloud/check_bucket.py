import boto3

class BucketChecker:
    def __init__(self):
        # Create an S3 client
        self.s3 = boto3.client('s3')

    def check_bucket_existence(self, bucket_name):
        """
        Check if a bucket exists on Amazon S3.

        Args:
        - bucket_name (str): The name of the bucket to check.

        Returns:
        - bool: True if the bucket exists, False otherwise.
        """
        try:
            # Try to head the bucket (a lightweight operation to check existence)
            self.s3.head_bucket(Bucket=bucket_name)
            return True
        except self.s3.exceptions.NoSuchBucket:
            # If NoSuchBucket exception is raised, the bucket does not exist
            return False
            