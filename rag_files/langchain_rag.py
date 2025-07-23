
from langchain.chains import RetrievalQA 
#from langchain.chains.summarize import load_summarize_chain
#chain = load_summarize_chain(llm, chain_type="refine")

def build_rag_chain(llm, embedding_vectors, task="qa"):

    if task == "qa":
        return RetrievalQA.from_chain_type(
            llm=llm,
            retriever=embedding_vectors.as_retriever(search_type="similarity", k=3),
            return_source_documents=False)
    else: 
        raise ValueError(f"{task} is unknown. Please use 'qa' for now.")


def query_system(question, rag_chain, task="qa", documents=None):
    """
    querying system based on given task
    Args:
    - rag_chain: The RAG chain (e.g., ConversationalRetrievalChain)
    - task: Task type ("qa")
    - documents: Only needed for future tasks like "summarize" or "refine"
    Returns:
    - answer from system based on query
    """
    if task in ["qa"]:
        response = rag_chain.invoke(question)
        return response

    else:
        raise ValueError(f"Unknown task: {task}")


