import boto3
from pathlib import Path
import requests
import os

def download_s3_folder(bucket: str, s3_path: str, destination_dir: str, print_downloaded_files: bool = False):
    """Download a folder from an S3 bucket to a local directory
    Args:
        bucket (str): Name of the S3 bucket
        s3_path (str): S3 Path (folder path) to download
        destination_dir (str): Local directory to save the downloaded files
        print_downloaded_files (bool): If True, prints the downloaded files with size
    """
    s3_client = boto3.client('s3') # to connect to S3 (AWS storage)
    paginator = s3_client.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=s3_path):
            keys = [obj["Key"] for obj in page.get("Contents", [])]
            for key in keys:
                if key.endswith("/"): # so S3 does not get confused
                    print(f"Skipping directory placeholder: {key}")
                    continue
                relative_path = Path(key).relative_to(s3_path)
                target_path = Path(destination_dir) / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    s3_client.download_file(bucket, key, str(target_path))
                except Exception as e:
                    print(f"Download of {key} failed: {e}")

        if print_downloaded_files:
            print("Downloaded model folder contents:")
            for path in Path(destination_dir).rglob("*"):
                    if path.is_file():
                        size_mb = path.stat().st_size / (1024 ** 2)
                        print(f"{path} — {size_mb:.2f} MB")
                    else:
                        print(f"{path} (directory)")

    except Exception as e:
        print(f"Error while downloading from S3  '{s3_path}': {e}")


def is_running_on_aws():
    # for ECS Fargate:
    if os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI") or os.environ.get("ECS_CONTAINER_METADATA_URI_V4"):
        print("running on AWS ECS Fargate")
        return True
    else: 
        print("not running on AWS ECS Fargate")
    # for EC2:
    try:
        return requests.get("http://169.254.169.254/latest/meta-data/", timeout=0.2).ok
    except requests.exceptions.RequestException:
        return False
    

def download_data_if_on_aws(bucket_name: str, S3_model_path: str, local_model_path: str):
    """loads from S3"""
    if is_running_on_aws():
        try:
            download_s3_folder(bucket_name, S3_model_path, local_model_path)
        except requests.exceptions.RequestException:
            print("encountered an error while downloading model from S3")
    else:
        print("skipping S3 download, because code is not running on AWS")