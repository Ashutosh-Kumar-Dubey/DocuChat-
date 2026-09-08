# Document AI Assistant

An enterprise-grade Retrieval-Augmented Generation (RAG) platform designed to extract instant, highly accurate insights from secure PDF documents. Built with a deeply optimized, highly scalable microservices architecture.

---

##  Live Demo
**Access the live application here:** https://doc2chat-ai.streamlit.app/


---

## Architecture Overview

The system is separated into a serverless frontend and a high-performance backend REST API, connected to cloud-native vector and inference engines.

- **Frontend:** Streamlit *(deployed on Streamlit Community Cloud)*
- **Backend API:** FastAPI *(deployed on Render)*
- **Vector Database:** Qdrant Cloud
- **Embedding Engine:** Hugging Face Serverless Inference API (`all-MiniLM-L6-v2`)
- **LLM Engine:** Groq API (`groq/compound`)

### System Flow

```mermaid
graph TD
    classDef frontend fill:#D8B4E2,stroke:#7B2CBF,stroke-width:2px,color:#000
    classDef backend fill:#C8B6E6,stroke:#7B2CBF,stroke-width:2px,color:#000
    classDef database fill:#9A8C98,stroke:#000,stroke-width:2px,color:#fff
    classDef ai fill:#7B2CBF,stroke:#D8B4E2,stroke-width:2px,color:#fff

    User([User])
    UI[Streamlit UI<br/>app.py]:::frontend
    API[FastAPI Backend<br/>main.py]:::backend
    Qdrant[(Qdrant Cloud<br/>Vector DB)]:::database
    HF{Hugging Face API<br/>Embeddings}:::ai
    Groq{Groq API<br/>LLM Inference}:::ai

    User -- Uploads PDF / Asks Question --> UI
    UI -- HTTP POST /api/upload --> API
    UI -- HTTP POST /api/query --> API
    
    API -- Chunks text --> HF
    HF -- Returns Vectors --> API
    API -- Upserts / Searches --> Qdrant
    
    API -- Injects Context --> Groq
    Groq -- Streams Answer --> API
    API -- Returns Answer --> UI
    UI -- Displays Insights --> User
```

---

## Data Ingestion Pipeline

The platform features a highly optimized, synchronous data ingestion pipeline that processes documents in real-time without relying on external message queues (like Inngest or Celery):

1. **Upload & Secure Transmission:** The user uploads a PDF via the Streamlit UI. The file is immediately streamed to the FastAPI backend via a secure `multipart/form-data` REST endpoint (`/api/upload`).
2. **Text Extraction & Chunking:** The backend utilizes LlamaIndex to parse the PDF and intelligently split the text into overlapping chunks (1000 tokens per chunk with 200 token overlap) to preserve semantic context.
3. **Cloud Vectorization:** Instead of taxing the local server's CPU with PyTorch, the chunks are sent to Hugging Face's Enterprise Router (`router.huggingface.co`). The `all-MiniLM-L6-v2` model generates 384-dimensional embeddings.
4. **Database Upsertion:** The vectors, along with the raw text payload and UUID metadata, are permanently indexed in Qdrant Cloud for instantaneous semantic retrieval.

---

## Core Features

- **Zero-Latency Embeddings:** Completely offloads heavy tensor operations to the Hugging Face Cloud, preventing server OOM (Out of Memory) crashes.
- **Stateless Architecture:** The backend API remains entirely stateless, allowing instantaneous cold boots on heavily constrained server environments.
- **Reference Tracking:** Automatically tracks and returns exact context chunks used to generate the LLM response to prevent AI hallucinations.
- **B2B UI/UX:** A highly responsive, single-page application built entirely in dark mode with a professional lavender accent palette.

---

## Project Structure

```text
Document-AI/
├── app.py                   # Streamlit frontend UI
├── main.py                  # FastAPI backend routing and endpoints
├── data_loader.py           # PDF parsing and Hugging Face API integration
├── vector_db.py             # Qdrant Database client and schema management
├── requirements.txt         # Frontend dependencies (Streamlit)
└── backend-requirements.txt # Backend dependencies (FastAPI, python-multipart)
```

---

## Environment Variables

The following secrets are required for deployment:

| Key | Description | Location |
| :--- | :--- | :--- |
| `QDRANT_URL` | The REST API URL of your Qdrant Cloud cluster | Backend (Render) |
| `QDRANT_API_KEY` | Authentication key for Qdrant | Backend (Render) |
| `GROQ_API_KEY` | API key for Groq's ultra-fast LLM routing | Backend (Render) |
| `HF_TOKEN` | Hugging Face read token for inference endpoints | Backend (Render) |
| `BACKEND_URL` | The deployed URL of the FastAPI server | Frontend (Streamlit) |

---
*Built using Streamlit, FastAPI, Hugging Face, and Groq.*
