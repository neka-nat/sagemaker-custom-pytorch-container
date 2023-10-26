#!/bin/bash

# profile引数をチェックする、引数がなければデフォルトのprofileを使う
if [ $# -eq 0 ]; then
  profile=default
else
  profile=$1
fi

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile ${profile})
TAG=`git rev-parse --short HEAD`
REPO=${AWS_ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/sagemaker-custom-pytorch-image
IMAGE_NAME=${REPO}:${TAG}

aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${IMAGE_NAME}
docker build -t ${IMAGE_NAME} -f ./Dockerfile .
docker push ${IMAGE_NAME}
