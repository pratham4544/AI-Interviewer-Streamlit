# FROM public.ecr.aws/lambda/python:3.10

# # Install minimal system dependencies
# RUN yum -y install gcc gcc-c++

# # Copy requirements file
# COPY requirements-lambda.txt .

# # Upgrade pip and install Python dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements-lambda.txt

# # Copy function code
# COPY . ${LAMBDA_TASK_ROOT}


# # Set the CMD to your handler
# CMD [ "lambda_handler.handler" ]


# Use official Python image as base
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for MongoDB libs etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
