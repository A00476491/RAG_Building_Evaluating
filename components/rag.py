from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import torch
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

# Function to generate embeddings
def generate_embeddings(embedding_model, texts):
    return embedding_model.encode(texts, show_progress_bar=True, batch_size=160, device=device)

def LLM(prompt, tokenizer, generator_model):

    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(generator_model.device)

    generated_ids = generator_model.generate(**model_inputs, max_new_tokens=128)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
    return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

def load_dataset(document_dataset):

    df = pd.read_csv(document_dataset, encoding='utf-8')
    documents = [f"title: {d[1]}.  text: {d[2]}" for d in df.values.tolist()]
    documents_id = [d[0] for d in df.values.tolist()]
    return documents, documents_id, df


# This our RAG which is organized in one function
def query_answering_system(query, document_dataset):
    """
    Given a query and a document dataset, this function retrieves relevant documents and generates an answer.

    Parameters:
    - query (str): The user's question.
    - document_dataset (str): Path to the CSV file containing news articles.

    Returns:
    - answer (str): Generated response based on retrieved documents.
    """ 

    # Indexing: map documents to embeddings
    embedding_model = SentenceTransformer('BAAI/bge-small-en').to(device)
    embedding_cache_path = os.path.abspath(os.path.join(current_dir, '../data/document_embeddings.npy'))
    documents, documents_id, df = load_dataset(document_dataset)
    if not os.path.exists(embedding_cache_path):
        documents_embedding = generate_embeddings(embedding_model, documents)
        np.save(embedding_cache_path, documents_embedding)
    else:
        documents_embedding = np.load(embedding_cache_path)

    # Query: retrieve top-3 articles
    k= 3
    query_embedding = generate_embeddings(embedding_model, [query])
    similarities = cosine_similarity(query_embedding, documents_embedding)
    most_similar_indices = similarities.argsort()[0][-k:][::-1]
    retrieved_docs = [documents[i] for i in most_similar_indices]
    retrieved_docs_id = [documents_id[i] for i in most_similar_indices]

    # Generation: LLM output
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B", trust_remote_code=True)
    generator_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B", torch_dtype=torch.float16).to(device)

    prompt = "Given the following documents:\n"
    prompt += "\n".join(f"{i+1}. {doc}" for i, doc in enumerate(retrieved_docs))
    prompt += f"\n\nUser query: {query}\n\n"
    prompt += "Based on the above documents, provide a concise, clear, and logically structured answer to the user's query.\n"
    prompt += "Only answer what is necessary for the question, under 40 words.\n"
    prompt += "If the necessary answer is too long, condense it into key phrases or a short summary.\n"
    prompt += "Avoid bullet points; respond in a fluid and natural sentence structure."
    answer = LLM(prompt, tokenizer, generator_model)


    # organize output
    output = {
        'answer': answer,
        'title': [df.loc[df['content_id'] == i, 'title'].values[0] for i in retrieved_docs_id],
        'retrieved_docs_id': retrieved_docs_id
    }
    return output

if __name__ == '__main__':

    query = "What was the net loss reported by 7-Eleven Malaysia Holdings Bhd for the fourth quarter ended December 31, 2024?"
    document_dataset = "../data/1K_news.csv"
    output = query_answering_system(query, document_dataset)

    print('Question: {}'.format(query))
    print('Answer: {}'.format(output['answer']))
    print('Reference1: {}'.format(output['title'][0]))
    print('Reference2: {}'.format(output['title'][1]))
    print('Reference3: {}'.format(output['title'][2]))


    '''
    Question: What was the net loss reported by 7-Eleven Malaysia Holdings Bhd for the fourth quarter ended December 31, 2024?
    
    Answer: The net loss reported by 7-Eleven Malaysia Holdings Bhd for the fourth quarter ended December 31, 2024 was RM2.66 mil.
    
    Reference1: 7-Eleven 4Q revenue rises to RM745mil
    Reference2: 7-Eleven expects inflationary pressures from external headwinds
    Reference3: Berjaya Corp net loss narrows to RM88.68mil in 2Q25
    '''


