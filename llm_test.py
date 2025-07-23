from utils.model_cpp_setup import load_llm
from config import LOCAL_MODEL_PATH

def generate_text(llama, prompt):
    # Generate text using the loaded LLaMA model
    response = llama(prompt, 
                                max_tokens=100,
                                temperature=0.7, 
                                stop=["<|eot_id>|"])
    
    return response

# Load the LLM
llama = load_llm(LOCAL_MODEL_PATH)

# Example prompt to generate text
prompt = "Tell me a joke"
output = generate_text(llama, prompt)

print(output["choices"][0]["text"].strip())