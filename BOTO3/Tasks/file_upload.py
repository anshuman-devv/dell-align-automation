import boto3
import logging
import argparse

logging.basicConfig(level=logging.INFO)
client = boto3.client('s3')

def upload_file(bucket_name, file_path, object_name=None):
    object_name = object_name or file_path.split('/')[-1]
    try:
        with open(file_path, 'rb') as f:
            client.put_object(Body=f, Bucket=bucket_name, Key=object_name)
        logging.info(f"Uploaded '{file_path}' to '{bucket_name}/{object_name}'")
    except Exception as e:
        logging.error(f"Upload failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket')
    parser.add_argument('file')
    parser.add_argument('--object_name')
    args = parser.parse_args()
    upload_file(args.bucket, args.file, args.object_name)
