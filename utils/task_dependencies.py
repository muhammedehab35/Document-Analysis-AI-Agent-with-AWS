from rag_files.preprocess_documents import load_all_documents
from rag_files.langchain_rag import query_system

def get_result_for_task(rag_chain, task, documents_folder, question, documents=None):
    """
    This function handles the logic for different tasks such as...(todo)
    """
    if task in ["summarize", "refine"]:
        if documents == None:
            documents = load_all_documents(documents_folder, add_metadata=True)
        response = query_system(question, rag_chain, task, documents)
    else:
        response = query_system(question, rag_chain, task)

    if isinstance(response, dict) and "result" in response:
        print(f"Result: {response['result']}")
        with open('output.txt', 'w') as f:
            f.write(response["result"])
    else:
        print(f"Result: {response}")
        with open('output.txt', 'w') as f:
            f.write(response["result"])
