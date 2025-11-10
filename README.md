# CCMP200
# Architecture Diagram
```text
User
  ↓
API Gateway (HTTP API)
  ↓
StartImageResizeFunction (Lambda)
  ↓
Step Functions → ImageResizerFunction (Lambda)
  ↓
Resized S3 Bucket
```

# Prerequisites
- AWS account with permissions to create Lambda, S3, Step Functions, and API Gateway resources
- Pillow (for Python) layer added to the resizer Lambda
- Two S3 buckets: (names should be unique)
- original-images-your_name
- resized-images-your_name

# Deployment Instructions
Create S3 Buckets
- original-images-jeffryserrano
- resized-images-jeffryserrano
  
Deploy Lambda Functions
- StartImageResizeFunction: triggers Step Functions
  - Set environment variable:
    - STATE_MACHINE_ARN = arn:aws:states:us-east-1:340914758420:stateMachine:ImageResizeStateMachine
- ImageResizerFunction: resizes and saves image
  - Set environment variable:
    - RESIZED_BUCKET = resized-images-jeffryserrano
      
Create Step Functions State Machine
- Name: ImageResizeStateMachine
- Definition includes a Task state that invokes ImageResizerFunction
  
Configure API Gateway
- Type: HTTP API
- Route: POST /start-resize
- Integration: Lambda proxy → StartImageResizeFunction
- Stage: prod
  
Add Lambda Permissions
- Allow API Gateway to invoke StartImageResizeFunction
- Allow S3 to invoke StartImageResizeFunction
- Test with Postman
- URL: https://qhot2ux2c5.execute-api.us-east-1.amazonaws.com/prod/start-resize
- Method: POST
- Body: 
```
{
  "bucket": "original-images-jovyserrano",
  "key": "test2.jpg"
}
```

- Sample Response

```
{
  "status": "STARTED",
  "executionArn": "arn:aws:states:us-east-1:123456789012:execution:ImageResizeStateMachine:abc123"
}
```

