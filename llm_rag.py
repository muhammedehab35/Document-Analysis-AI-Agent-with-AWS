
import time
import os
from config import S3_BUCKET_NAME, S3_MODEL_PATH, LOCAL_MODEL_PATH, DOCS_FOLDER, TASK, S3_DOCS_FOLDER, QUESTION, S3_EMBEDDING_MODEL_PATH, LOCAL_EMBEDDING_MODEL_PATH, LOCAL_MODEL
from utils.aws_utils import download_data_if_on_aws
from utils.model_cpp_setup import load_llm
from rag_files.preprocess_documents import preprocess_documents, load_all_documents, load_vector_storage
from rag_files.langchain_rag import build_rag_chain
from utils.task_dependencies import get_result_for_task
#from utils.container_checks import print_all_env_variables

def main(s3_bucket_name, s3_model_path, s3_docs_folder, s3_embedding_model_path,
                local_model_path, local_docs_folder, local_embedding_model_path, local_model,
                task, question):
    print("Running app test!")
    #print_all_env_variables()

    # if running on AWS, download the model, the documents and the embedding model from S3
    download_data_if_on_aws(s3_bucket_name, s3_model_path, local_model_path)
    download_data_if_on_aws(s3_bucket_name, s3_docs_folder, local_docs_folder)
    download_data_if_on_aws(s3_bucket_name, s3_embedding_model_path, s3_embedding_model_path)

    # loading model and retriever
    llm = load_llm(local_model)

    # load prepocessed embedding vectors if available
    # if not, load documents from folder and preprocess them
    if os.path.exists("vector_db") and os.listdir("vector_db"):
        embedding_vectors = load_vector_storage()
        documents = None
    else:
        # loading documents
        documents = load_all_documents(local_docs_folder, add_metadata=True)
        # preprocessing documents / getting embedding vectors
        embedding_vectors = preprocess_documents(documents, local_embedding_model_path, save_preprocessed=True)
    
    # building RAG chain: pick a task (qa, chat, summarize, refine, sources)
    rag_chain = build_rag_chain(llm, embedding_vectors, task)

    get_result_for_task(rag_chain, task, local_docs_folder, question, documents=None)

    time.sleep(10)

if __name__ == "__main__":
    main(S3_BUCKET_NAME, S3_MODEL_PATH, S3_DOCS_FOLDER, S3_EMBEDDING_MODEL_PATH,
                LOCAL_MODEL_PATH, DOCS_FOLDER, LOCAL_EMBEDDING_MODEL_PATH, LOCAL_MODEL,
                TASK, QUESTION)

