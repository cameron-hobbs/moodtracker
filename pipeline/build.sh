#!/bin/bash

pip install awsebcli

cd staging/ || exit

eb init --region eu-west-1 moodtracker

mv ../../../frontend/build/* ../../src/frontend_build

cd ../../src || exit

echo "Now in src"

# needs to be ARM since that's what ec2 t4g runs
docker buildx build --platform=linux/arm64 -t moodtracker-api:0.1 .

docker tag moodtracker-api:0.1 725415724245.dkr.ecr.eu-west-1.amazonaws.com/moodtracker-api:latest

# get ecr password from aws cli: `aws ecr get-login-password --region eu-west-1`
docker login --username AWS --password "${ECR_PASSWORD}" 725415724245.dkr.ecr.eu-west-1.amazonaws.com

docker push 725415724245.dkr.ecr.eu-west-1.amazonaws.com/moodtracker-api:latest
