import logging
from file_upload import client

file = client.download_file('AnshumanS3Bucket', 'Akshita_Khandelwal_Resume.pdf', './Akshita_Khandelwal_Resume.pdf')

if file:
    logging.info(f"File {file} downloaded successfully")
    import logging
from pathlib import Path
from file_upload import client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_file(bucket_name: str, key: str, local_path: str):
    try:
        client.download_file(bucket_name, key, local_path)
        logging.info(f"File '{Path(key).name}' downloaded successfully to '{local_path}'")
    except Exception as e:
        logging.error(f"Failed to download file '{Path(key).name}': {e}")

if __name__ == "__main__":
    BUCKET_NAME = "YourS3Bucket"
    FILE_KEY = "YourFile.pdf"
    LOCAL_PATH = Path("./YourFile.pdf")

    download_file(BUCKET_NAME, FILE_KEY, str(LOCAL_PATH))
