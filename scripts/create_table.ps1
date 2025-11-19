$TABLE_NAME = $env:JOKES_TABLE
if (-not $TABLE_NAME) {
    $TABLE_NAME = "Jokes"
}

awslocal dynamodb create-table `
    --table-name $TABLE_NAME `
    --attribute-definitions AttributeName=id,AttributeType=S `
    --key-schema AttributeName=id,KeyType=HASH `
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

Write-Host "Table $TABLE_NAME created."
