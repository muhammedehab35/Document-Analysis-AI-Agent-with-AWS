# slim python base image from Docker Hub
FROM python:3.12-slim

# working directory for the application
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    cmake build-essential git wget curl \
    && rm -rf /var/lib/apt/lists/*
    
# for AWS deployment:
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# for local development, copy the local files into the container
#COPY requirements.txt /app/requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# (eventually) expose the port 
#EXPOSE 80

# start the application
CMD ["python", "llm_rag.py"]
