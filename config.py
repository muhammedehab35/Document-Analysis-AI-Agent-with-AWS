
# S3 related variables
S3_BUCKET_NAME = 'doc-task-bucket-1'

# llama-cpp model related variables
S3_MODEL_PATH = 'models/llama_cpp/'
LOCAL_MODEL_PATH= "models/llama_cpp/"
LOCAL_MODEL="models/llama_cpp/Llama-3.2-1B-Instruct-Q8_0.gguf"
DOCS_FOLDER = "documents/"
S3_DOCS_FOLDER = 'documents/'
S3_EMBEDDING_MODEL_PATH = "models/models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2/"
LOCAL_EMBEDDING_MODEL_PATH = "models/models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2/snapshots/86741b4e3f5cb7765a600d3a3d55a0f6a6cb443d"

# RAG related variables
EMBEDDING_MODEL_NAME = "models/sentence_transformer_paraphrase-multilingual-MiniLM-L12-v2/snapshots/86741b4e3f5cb7765a600d3a3d55a0f6a6cb443d"
FAISS_INDEX_PATH = "vector_db/faiss_index"

# adapt if necessary
TASK ="qa" # current options: qa           # summarize, chat, refine, sources are still in development
CHUNK_SIZE = 300  # 300 recommended for qa (if context length of model is only 512)
QUESTION = "In welchen Bereichen soll die Digitalisierung vorangebracht werden?"

