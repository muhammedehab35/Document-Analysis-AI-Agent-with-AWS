import os
import glob
#import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from config import CHUNK_SIZE
from sklearn.metrics.pairwise import cosine_similarity
#from langchain.docstore.document import Document

from config import FAISS_INDEX_PATH, EMBEDDING_MODEL_NAME

# === LOAD DOCS FROM FOLDER ===
def load_all_documents(folder_path, add_metadata=False):
    # check if the folder exists and is not empty
    if os.path.exists(folder_path) and os.listdir(folder_path):
        print(f"Loading documents from {folder_path}...")
        docs = []
        for file_path in glob.glob(os.path.join(folder_path, "*")):
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                continue

            loaded_docs = loader.load()

            if add_metadata:
                # Add source metadata (filename) to each document
                filename = os.path.basename(file_path)
                for doc in loaded_docs:
                    doc.metadata["source"] = filename
                    #print(f"--------------DOCUMENT METADATA: {doc.metadata=}----------------")

            docs.extend(loaded_docs)
            return docs
    else:
        raise ValueError(f"No documents found in {folder_path}")
    

# === CHUNKING ===
def chunk_documents(documents):
    # Split the documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=20)
    #splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=20)
    split_docs = splitter.split_documents(documents)
    return split_docs

# === REMOVE REDUNDANT AND OUTLIER EMBEDDINGS ===
def reduce_embeddings(embedding_index, similarity_threshold=0.9):
    ...

# === PREPROCESS DOCS ===
def preprocess_documents(documents, local_embedding_model_path , save_preprocessed=False):
    splitted_docs = chunk_documents(documents)
    #embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    embedding_model = HuggingFaceEmbeddings(model_name=local_embedding_model_path)
    embedding_vectors = FAISS.from_documents(splitted_docs, embedding_model)
    if save_preprocessed:
        embedding_vectors.save_local(FAISS_INDEX_PATH)
    return embedding_vectors

# === LOAD PREPROCESSED DOCS IF STORED BEFORE ===
def load_vector_storage():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)