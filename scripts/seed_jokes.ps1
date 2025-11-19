$FunctionName = "JokeFunction"
$RoleArn = "arn:aws:iam::000000000000:role/lambda-ex"  # Dummy role for LocalStack

# Remove old build directory if it exists
if (Test-Path "build") {
    Remove-Item "build" -Recurse -Force
}

# Create build directory
New-Item -ItemType Directory -Path "build" | Out-Null

# Install dependencies into build/
pip install -r ../requirements.txt -t build

# Copy source code into build/
Copy-Item -Path "../src/*" -Destination "build" -Recurse

# Create lambda.zip from the contents of build/
if (Test-Path "../lambda.zip") {
    Remove-Item "../lambda.zip" -Force
}

Compress-Archive -Path "build\*" -DestinationPath "../lambda.zip" -Force

Set-Location ..

# Check if the Lambda already exists
awslocal lambda get-function --function-name $FunctionName *> $null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Updating existing Lambda..."
    awslocal lambda update-function-code `
        --function-name $FunctionName `
        --zip-file fileb://lambda.zip | Out-Null
}
else {
    Write-Host "Creating Lambda..."
    awslocal lambda create-function `
        --function-name $FunctionName `
        --runtime python3.11 `
        --handler src.handler.lambda_handler `
        --role $RoleArn `
        --environment "Variables={JOKES_TABLE=Jokes,DYNAMODB_ENDPOINT=http://localhost:4566}" `
        --zip-file fileb://lambda.zip | Out-Null
}

Write-Host "Lambda $FunctionName deployed."
