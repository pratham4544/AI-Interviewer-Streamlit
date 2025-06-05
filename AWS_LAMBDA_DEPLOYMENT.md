# Deploying Rupadi AI Interviewer to AWS Lambda

This guide will help you deploy the Rupadi AI Interviewer API to AWS Lambda using Docker containers.

## What's Changed

The application has been converted from a Streamlit web app to a FastAPI-based REST API that can be deployed to AWS Lambda. Here's what's changed:

- `api.py`: New FastAPI application that provides all core functionality as API endpoints
- `lambda_handler.py`: AWS Lambda handler that wraps the FastAPI app using Mangum
- `requirements-lambda.txt`: Updated dependencies for Lambda deployment
- `Dockerfile`: Updated for Lambda container deployment

## API Endpoints

The API provides the following endpoints:

- `GET /` - Health check endpoint
- `GET /candidates` - List all available candidates
- `POST /prepare-interview` - Extract candidate info and generate questions
- `GET /interview/{candidate_id}` - Get stored interview questions for a candidate
- `POST /evaluate-answer` - Evaluate a candidate's answer to a question
- `POST /generate-follow-up` - Generate a follow-up question based on previous answer
- `GET /results/{candidate_id}` - Get the interview results for a candidate

## Deployment Steps

### 1. Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker installed

### 2. Set up Environment Variables

Ensure your environment variables are properly set in AWS Lambda. You'll need:

- `GROQ_API_KEY`: Your Groq API key
- `MONGO_URI`: Your MongoDB connection string

### 3. Build and Deploy the Docker Image

```bash
# Build the Docker image
docker build -t rupadi-interviewer-api .

# Log in to AWS ECR
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com

# Create an ECR repository (if it doesn't exist)
aws ecr create-repository --repository-name rupadi-interviewer-api

# Tag and push the image
docker tag rupadi-interviewer-api:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/rupadi-interviewer-api:latest
docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/rupadi-interviewer-api:latest
```

### 4. Create Lambda Function

1. Go to AWS Lambda console
2. Create a new function
3. Select "Container image" as the deployment package type
4. Browse for the ECR image you pushed
5. Configure memory (recommended: at least 512MB) and timeout (at least 30 seconds)
6. Add environment variables (GROQ_API_KEY, MONGO_URI)

### 5. Configure API Gateway

1. Create a new API Gateway (HTTP API or REST API)
2. Create a route that integrates with your Lambda function
3. Deploy the API

## Testing Locally

Before deploying to AWS, you can test the API locally:

```bash
# Run the API locally
python lambda_handler.py
```

This will start the API server on http://0.0.0.0:8000

## Important Notes

1. The API removes the audio recording/playback functionality since Lambda functions are stateless
2. MongoDB is still used for data persistence
3. Ensure your MongoDB instance is accessible from AWS Lambda (consider using MongoDB Atlas)
4. Consider AWS Lambda throttling and timeout limits for your use case

## Troubleshooting

- If you encounter memory issues, increase the Lambda function's memory allocation
- If your function times out, increase the timeout setting
- Check CloudWatch Logs for detailed error messages
