from langchain_community.llms import LlamaCpp

def load_llm(model_path):
    # Load the LLaMA model with llama-cpp-python
    llama = LlamaCpp(model_path=model_path, max_tokens=512) #, n_ctx=512, n_batch=8, temperature=0.1, top_p=0.95, repeat_penalty=1.2)
    
    print("Model loaded successfully")
    
    return llama