#!/bin/bash

set -e

echo "========================================"
echo "Packaging Fetch Lambda"
echo "========================================"

cd lambda/fetch_lambda
zip -r ../../fetch_lambda.zip .
cd ../..

echo "========================================"
echo "Packaging ETL Lambda"
echo "========================================"

cd lambda/etl_lambda
zip -r ../../etl_lambda.zip .
cd ../..

echo "========================================"
echo "Deploying Fetch Lambda"
echo "========================================"

aws lambda update-function-code \
    --function-name earthquake-fetch-lambda \
    --zip-file fileb://fetch_lambda.zip

echo "========================================"
echo "Deploying ETL Lambda"
echo "========================================"

aws lambda update-function-code \
    --function-name earthquake-etl-lambda \
    --zip-file fileb://etl_lambda.zip

echo "========================================"
echo "Deployment Completed Successfully"
echo "========================================"