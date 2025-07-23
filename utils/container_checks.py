import os
import boto3

def print_all_env_variables():
    # all environment variables as a dictionary
    env_vars = os.environ
    # print environment variables + values
    for key, value in env_vars.items():
        print(f"{key}={value}")


def check_boto3_credentials():
    session = boto3.Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    print("Boto3 AWS Access Key ID:", current_credentials.access_key)
    print("Boto3 AWS Secret Access Key:", current_credentials.secret_key)
    print("Boto3 AWS Session Token:", current_credentials.token)


def print_filesystem_tree(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # recursively walk through the directory tree and 
        # print directory names and file names
        print(f"Directory: {dirpath}")
        print(f"Subdirectories: {dirnames}")
        print(f"Files: {filenames}")
        print("-" * 40)

# print_filesystem_tree("/app")  
