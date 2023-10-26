import subprocess

import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator


def get_latest_commit_hash(repo_path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=repo_path).decode("utf-8").strip()

bucket = "sagemaker-test-bucket-0001"
prefix = "sagemaker/custom-pytorch-container"
role_name = "AmazonSageMaker-ExecutionRole-20231026T191440"

sagemaker_session = sagemaker.Session()
account_id = boto3.client("sts").get_caller_identity().get("Account")
iam = boto3.client('iam')
role = iam.get_role(RoleName=role_name)["Role"]["Arn"]
tag = get_latest_commit_hash(".")
image_uri = f"{account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/sagemaker-custom-pytorch-image:{tag}"
print("image_uri:", image_uri)


estimator = Estimator(
    image_uri=image_uri,
    role=role,
    instance_count=1,
    instance_type="ml.p2.xlarge",
    output_path=f"s3://{bucket}/{prefix}/output",
    hyperparameters={"epochs": 5, "save_model": True},
    sagemaker_session=sagemaker_session)

estimator.fit()
