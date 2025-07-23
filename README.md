# AI Agent for Document Analysis with AWS

## AWS services used

- ECR (Elastic Cloud Repository) for docker containers
- S3 (for storage)
- ECS Fargate (for deployment of containers)

## Frameworks / Tools

- Embedding Model
- Faiss (in-memory vector store & search)
- Langchain (for RAG)

## RAG

Retrieval augmented generation with task specification options:

- default: Q&A (with cosine similarity)

for future development and models with larger context lenth:

- "sources" (Q&A with sources - with similarity_score_threshold)
- "summarize" (with maximum marginal relevance)
- "refine" (summarize short and precise - with cosine similarity)
- "chat" (with memory - and dynamic mmr)

## UI

under development...
for now, the question is hardcoded in llm_rag.py

## Models

For efficient use with an AWS Free Tier account, the setup can be used with small models, which works well, but impacts the quality of the RAG.
The used models are sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 as
Emebdding Model and Llama-3.2-1B-Instruct as Tiny LLM.
Unfortunately, the used Llama-3.2-1B-Instruct only generates poorly in German. For better German language skills, choose a different model.

They can be downloaded from huggingface and uploaded to S3:

- [EMBEDDING MODEL](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- [Tiny LLM](https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF)

The workflow is setup to be plug and play for different models.
To run the models locally or on a paid AWS account, you can
use it with bigger models, especially with an LLM with larger context length
and better multilingual support.

## Github Action Workflow

- github action workflow is set up to automate the process and start the ECS deployment of the container
- if application code changes (except for README, .dockerignore and github workflow files) the container is rebuilt and pushed to the ECR
- if anything is pushed on the github repo, this triggers the deployment of the code on AWS ECS

SETUP on AWS:

- set up ECS Fargate with proper compute (1 CPU with max 5GB should be enough for the start) and the docker image-URI
- set up an S3 bucket for the project and upload the model to it
- in the IAM the ecsTaskExecutionRole needs to be selected and an AmazonS3ReadOnlyAccess permission attatched to it
- a TaskRole needs to be set up (self configured),
with AmazonS3ReadOnlyAccess permission
(this is needed for the container to get credentials for the S3 buckets)

The new task definition within the actions workflow needs to be set with the following parameters:

```bash
family: .family,
containerDefinitions: .containerDefinitions, 
requiresCompatibilities: ["FARGATE"], 
networkMode: "awsvpc", 
executionRoleArn: .executionRoleArn, 
taskRoleArn: .taskRoleArn, 
cpu: .cpu, 
memory: .memory
```

Check my github action yml file on how to do this.
Some parameters are not hardcoded and can also be set
up in first in AWS ECS - Task Definitions:

- for cpu: 2vCPU are recommended
- for memory: 5-7GB are recommended

## Commands for manual upload of the docker container

- build docker container

```bash
docker build -t aws_docker_image .
```

- giving the container a name tag that relates to the ECR (add resource in ECR first with AWS in browser):

```bash
docker tag aws_docker_image <aws_ID...amazonaws.com>
```

- after installing AWS CLI: enter the user / person access code for AWS CLI

```bash
aws config
```

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.eu-central-1.amazonaws.com
```

this should output: Login Succeeded

- then push the docker container to AWS ECR:

```bash
docker push <aws_ID...amazonaws.com>
```

- for local development build the docker with file mount:

```bash
docker run -v /path/to/local/files:mount/path <image_name>
```
