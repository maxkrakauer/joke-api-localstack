$FunctionName = "JokeFunction"

# Create the REST API
$restApiId = awslocal apigateway create-rest-api `
    --name JokeApi `
    --query 'id' `
    --output text

# Get the root resource ID ("/")
$rootId = awslocal apigateway get-resources `
    --rest-api-id $restApiId `
    --query 'items[0].id' `
    --output text

# Create /jokes resource
$resourceId = awslocal apigateway create-resource `
    --rest-api-id $restApiId `
    --parent-id $rootId `
    --path-part jokes `
    --query 'id' `
    --output text

# Configure GET and POST methods
foreach ($method in @("GET", "POST")) {
    awslocal apigateway put-method `
        --rest-api-id $restApiId `
        --resource-id $resourceId `
        --http-method $method `
        --authorization-type "NONE" | Out-Null

    awslocal apigateway put-integration `
        --rest-api-id $restApiId `
        --resource-id $resourceId `
        --http-method $method `
        --type AWS_PROXY `
        --integration-http-method POST `
        --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:$FunctionName/invocations" | Out-Null
}

# Allow API Gateway to invoke the Lambda
awslocal lambda add-permission `
    --function-name $FunctionName `
    --statement-id apigw-test `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:us-east-1:000000000000:$restApiId/*/*/jokes" | Out-Null

# Deploy the API to the "dev" stage
awslocal apigateway create-deployment `
    --rest-api-id $restApiId `
    --stage-name dev | Out-Null

# Build the URL
$apiUrl = "http://localhost:4566/restapis/$restApiId/dev/_user_request_/jokes"

# Save it to a file at project root: .last_api_url
$projectRoot = Resolve-Path "$PSScriptRoot\.."
$apiFilePath = Join-Path $projectRoot ".last_api_url"
$apiUrl | Out-File -FilePath $apiFilePath -Encoding utf8

Write-Host "API ID: $restApiId"
Write-Host "API URL: $apiUrl"
Write-Host "Saved to: $apiFilePath"
