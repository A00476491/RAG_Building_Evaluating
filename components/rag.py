from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import torch
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))

# This our RAG which is organized in one function
def query_answering_system(query, document_dataset, embedding_model_name='BAAI/bge-small-en', model_name="Qwen/Qwen2.5-0.5B", k=3, embedding_cache_path='../data/document_embeddings.npy'):
    """
    Given a query and a document dataset, this function retrieves relevant documents and generates an answer.

    Parameters:
    - query (str): The user query.
    - document_dataset (str): Path to the CSV file containing documents with 'title' in column index 1 and 'text' in column index 2.
    - embedding_model_name (str): Name of the sentence embedding model.
    - model_name (str): Name of the language model.
    - k (int): Number of top similar documents to retrieve.
    - embedding_cache_path (str): Path to store/load document embeddings.

    Returns:
    - answer (str): Generated response based on retrieved documents.
    """
    
    # Check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.cuda.empty_cache()

    # Load pre-trained models
    embedding_model = SentenceTransformer(embedding_model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    generator_model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to(device)

    # Load dataset
    df = pd.read_csv(document_dataset, encoding='utf-8')
    documents = [f"title: {d[1]}.  text: {d[2]}" for d in df.values.tolist()]

    # Function to generate embeddings
    def generate_embeddings(texts):
        return embedding_model.encode(texts, show_progress_bar=True, batch_size=160, device=device)

    # Generate/load document embeddings
    embedding_cache_path = os.path.abspath(os.path.join(current_dir, embedding_cache_path))
    if not os.path.exists(embedding_cache_path):
        documents_embedding = generate_embeddings(documents)
        np.save(embedding_cache_path, documents_embedding)
    else:
        documents_embedding = np.load(embedding_cache_path)

    # Retrieve top-k similar documents
    query_embedding = generate_embeddings([query])
    similarities = cosine_similarity(query_embedding, documents_embedding)
    most_similar_indices = similarities.argsort()[0][-k:][::-1]
    retrieved_docs = [documents[i] for i in most_similar_indices]

    # Construct the prompt
    prompt = "Given the following documents:\n"
    prompt += "\n".join(f"{i+1}. {doc}" for i, doc in enumerate(retrieved_docs))
    prompt += f"\n\nUser query: {query}\n\n"
    prompt += "Based on the above documents, provide a concise, clear, and logically structured answer to the user's query.\n"
    prompt += "Also please give me the basis for your answer."

    # Generate response
    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(generator_model.device)

    generated_ids = generator_model.generate(**model_inputs, max_new_tokens=512)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
    answer = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    output = {
        'answer': answer,
        'title': [
            re.search(r'title:\s*(.*?)\s*text:', doc).group(1).strip()
            for doc in retrieved_docs if re.search(r'title:\s*(.*?)\s*text:', doc)
        ]
    }

    return output

if __name__ == '__main__':
    query = "What option do civil servants in Malaysia have for their working hours during Ramadan, according to Communications Minister Fahmi Fadzil?"
    document_dataset = "../data/1K_news.csv"
    output = query_answering_system(query, document_dataset)
    print(output)


