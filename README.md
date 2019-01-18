# json-logs-to-kinesis-firehose

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiOHM1dnF0dkwvUE1WQ2NzMnNwSTZraXQrYXhSR1Q3dTVRRnMzVWVTU1RYR2VVVlArR2s1VVZrUVk2allsdExZaTFiN0tmWTZNWm0zZ21tbWcrWFlCVmRzPSIsIml2UGFyYW1ldGVyU3BlYyI6IkVlR1N4MmdNRzZwdGhST1QiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This serverless application forwards JSON-formatted log events for a given CloudWatch Log Group to a Kinesis Data Firehose Delivery Stream. Any log events that are not recognized as valid JSON are skipped.

## App Architecture

![App Architecture](https://github.com/jlhood/json-lambda-logs-to-kinesis-firehose/raw/master/images/app-architecture.png)

1. Lambda function is subscribed to the given CloudWatch log group name.
1. Any log event that is recognized as JSON are sent to the given Kinesis Delivery Stream.
1. If the given Log Group does not exist when this app is deployed, the app automatically creates one with default settings. This is useful for Lambda functions, which create the log group on first invoke.

## Installation Instructions

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, visit the [app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:277187709615:applications/json-logs-to-kinesis-firehose). Click the "Copy as SAM Resource" button and paste the copied YAML into your SAM template, filling in any required parameters. Alternatively, you can deploy the application into your account directly via the AWS Lambda Console.

## App Parameters

1. `LogGroupName` (required) - Name (not ARN) of the log group whose JSON-formatted logs should be sent to the given Kinesis Data Firehose Delivery Stream.
1. `KinesisFirehoseDeliveryStream` (required) - Name (not ARN) of the Kinesis Data Firehose Delivery Stream that JSON-formatted log events should be written to.
1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO

## App Outputs

1. `ForwardJsonLogsFunctionName` - Log forwarding Lambda function name.
1. `ForwardJsonLogsFunctionArn` - Log forwarding Lambda function ARN.

## License Summary

This code is made available under the MIT license. See the LICENSE file.
