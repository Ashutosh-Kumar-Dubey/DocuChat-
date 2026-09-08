import os
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from openai import OpenAI

EMBED_DIM = 384
splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)

def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, 'text', None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) -> list[list[float]]:
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token:
        raise ValueError('HF_TOKEN environment variable is not set!')
        
    client = OpenAI(api_key=hf_token, base_url='https://router.huggingface.co/hf-inference/v1')
    response = client.embeddings.create(model='sentence-transformers/all-MiniLM-L6-v2', input=texts)
    return [r.embedding for r in response.data]
