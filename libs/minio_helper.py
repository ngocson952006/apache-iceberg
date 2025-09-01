import os
import pandas as pd
import logging

endpoint_url = os.getenv("STORAGE_URI", "http://localhost:9000")
access_key = os.getenv("MINIO_ACCESS_KEY", "admin")
secret_key = os.getenv("MINIO_SECRET_KEY", "password")

storage_options = {
    "key": access_key,
    "secret": secret_key,
    "client_kwargs": {"endpoint_url": endpoint_url},
    "config_kwargs": {"s3": {"addressing_style": "path"}},
    "use_ssl": False
}

# make sure s3fs is installed from the running machine
try:
    import s3fs
except ImportError:
    raise ImportError("s3fs is not installed. Please install it with 'pip install s3fs'")


def read_csv(bucket: str, key: str, **kwargs):
    """
    Reads a CSV file from an S3 bucket and returns a DataFrame. The function constructs the file path
    using the bucket name and key, and utilizes `pandas.read_csv` to read the data. Additional keyword
    arguments can be passed to further customize the behavior of `pandas.read_csv`.

    :param bucket: The name of the S3 bucket containing the CSV file.
    :type bucket: str
    :param key: The key or file path within the S3 bucket for the desired CSV file.
    :type key: str
    :param kwargs: Additional keyword arguments to be passed to `pandas.read_csv`.
    :return: A DataFrame containing the data from the specified CSV file.
    :rtype: pandas.DataFrame
    :raises Exception: If the `s3fs` module is not installed.
    """
    try:
        logging.info(f"Reading CSV file from S3 bucket {bucket} with key {key}")
        df =  pd.read_csv(f"s3://{bucket}/{key}", storage_options=storage_options, **kwargs)
        logging.info(f"Read file: ${key} CSV file successfully")
        return df
    except Exception as e:
        logging.error(f"Error reading CSV file from S3 bucket {bucket} with key {key}: {e}")
        raise Exception(f"Error reading CSV file from S3 bucket {bucket} with key {key}: {e}")

def minio_client():
    """
    Creates and returns an instance of S3FileSystem using the parameters provided
    in the `storage_options`.

    The function initializes an object for interacting with the MinIO storage system,
    allowing for operations such as reading and writing files to an S3-compatible
    storage backend.

    :raises Exception: If any error occurs while creating the S3FileSystem instance.

    :return: An instance of `s3fs.S3FileSystem` configured with the provided
             `storage_options`.
    :rtype: s3fs.S3FileSystem
    """
    try:
       return s3fs.S3FileSystem(**storage_options)
    except Exception as e:
        raise Exception(f"Error creating S3FileSystem: {e}")

def upload_file(s3fs: s3fs.S3FileSystem, bucket: str, file_path: str, remote_path: str = None):
    """
    Uploads a file to an S3 bucket using the provided S3FileSystem instance. The method
    attempts to upload the file at the specified local path to the bucket under the given
    remote path or uses the filename of the local file as the S3 key if no remote path
    is provided. Logs progress and errors during the upload process.

    :param s3fs: S3 filesystem instance used to interact with the S3 bucket.
                 Must be properly initialized.
    :type s3fs: s3fs.S3FileSystem

    :param bucket: Name of the target S3 bucket where the file will
                   be uploaded.
    :type bucket: str

    :param file_path: Path to the local file that needs to be uploaded.
    :type file_path: str

    :param remote_path: (Optional) Path within the bucket where the file
                        will be stored. Defaults to the base name of
                        the local file.
    :type remote_path: str

    :return: True if the file has been successfully uploaded, False otherwise.
    :rtype: bool
    """
    if not s3fs:
        raise Exception("S3FileSystem not initialized")
    if not remote_path:
        remote_path = os.path.basename(file_path)
    try:
        logging.info(f"Uploading file {file_path} to S3 bucket {bucket} with key {remote_path}")
        s3fs.put(file_path, remote_path, bucket_name=bucket)
        logging.info(f"Uploaded file {file_path} to S3 bucket {bucket} with key {remote_path}")

        return True
    except FileNotFoundError as e:
        logging.error(f"File {file_path} not found: {e}")
        return False
    except Exception as e:
        logging.error(f"Error uploading file {file_path} to S3 bucket {bucket}: {e}")
        return False

def upload_df_to_remote(s3fs: s3fs.S3FileSystem, bucket: str, df: pd.DataFrame, remote_path: str):
    """
    Uploads a Pandas DataFrame to a specified remote path within an S3 bucket using
    the specified S3FileSystem. The function returns a boolean indicating success
    or failure.

    This function writes the DataFrame in CSV format to the specified S3 remote
    path. If the upload is unsuccessful, an error is logged and False is returned.
    The destination path is formed by combining the bucket name and remote path.

    :param s3fs: The initialized S3FileSystem object used for authentication
                 and interaction with the S3 service.
    :type s3fs: s3fs.S3FileSystem
    :param bucket: The name of the S3 bucket where the DataFrame will be stored.
    :type bucket: str
    :param df: The Pandas DataFrame object to be uploaded to the S3 bucket.
    :type df: pd.DataFrame
    :param remote_path: The path within the specified S3 bucket where the DataFrame
                        will be uploaded.
    :type remote_path: str
    :return: A boolean indicating whether the upload was successful.
    :rtype: bool
    """
    if not s3fs:
        logging.error("S3FileSystem not initialized")
        return False
    destination_path = f"s3://{bucket}/{remote_path}"
    logging.info(f"Uploading dataframe to {destination_path}")
    try:
        df.to_csv(destination_path, index=False, storage_options=storage_options)
        logging.info(f"Uploaded dataframe to {destination_path}")
        return True
    except Exception as e:
        logging.error(f"Error uploading dataframe to {destination_path}: {e}")
        return False