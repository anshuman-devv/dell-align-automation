import logging
from file_upload import client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def list_s3_objects(bucket_name: str):
    try:
        response = client.list_objects(Bucket=bucket_name)
        objects = response.get("Contents", [])

        if not objects:
            logging.info(f"No objects found in bucket '{bucket_name}'.")
            return

        for obj in objects:
            file_name = obj.get("Key", "Unknown")
            file_size = obj.get("Size", "Unknown")
            logging.info(f"Name: {file_name}, Size: {file_size} bytes")

    except Exception as e:
        logging.error(f"Failed to list objects in bucket '{bucket_name}': {e}")

if __name__ == "__main__":
    BUCKET_NAME = "YourS3Bucket"
    list_s3_objects(BUCKET_NAME)
