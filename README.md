# Document AI Assistant

An enterprise-grade Retrieval-Augmented Generation (RAG) platform designed to extract instant, accurate insights from secure PDF documents. Built with a deeply optimized, lightweight microservices architecture.

## Architecture Overview

The system is separated into a serverless frontend and a high-performance backend REST API, connected to cloud-native vector and inference engines.

- **Frontend:** Streamlit (deployed on Streamlit Community Cloud)
- **Backend API:** FastAPI (deployed on Render)
- **Vector Database:** Qdrant Cloud
- **Embedding Engine:** Hugging Face Serverless Inference API (\ll-MiniLM-L6-v2\)
- **LLM Engine:** Groq API (\groq/compound\)

### System Flow
1. **Ingestion:** Secure PDFs are uploaded via the Streamlit frontend and securely transmitted to the FastAPI backend.
2. **Processing:** The backend extracts the text, generates vector embeddings via Hugging Face's enterprise router, and indexes them in Qdrant Cloud.
3. **Querying:** User queries are embedded and searched against Qdrant. The relevant context is dynamically injected into a prompt and processed by Groq's ultra-low-latency LLM network to generate a highly accurate, deterministic response.

## Core Features
- **Zero-Latency Embeddings:** Completely offloads heavy PyTorch tensor operations to the Hugging Face Cloud, preventing server OOM crashes.
- **Stateless Architecture:** The backend API remains entirely stateless, allowing instantaneous cold boots on heavily constrained server environments.
- **Reference Tracking:** Automatically tracks and returns exact context chunks used to generate the LLM response to prevent hallucinations.
- **B2B UI/UX:** A highly responsive, single-page application built entirely in dark mode with a professional lavender accent palette.

## Project Structure
\\\	ext
+-- app.py                 # Streamlit frontend UI
+-- main.py                # FastAPI backend routing and endpoints
+-- data_loader.py         # PDF parsing and Hugging Face API integration
+-- vector_db.py           # Qdrant Database client and schema management
+-- requirements.txt       # Frontend dependencies
+-- backend-requirements.txt # Backend dependencies
\\\`n
## Environment Variables
The following secrets are required for deployment:
- \QDRANT_URL\: The REST API URL of your Qdrant Cloud cluster.
- \QDRANT_API_KEY\: Authentication key for Qdrant.
- \GROQ_API_KEY\: API key for Groq's LLM routing.
- \HF_TOKEN\: Hugging Face read token for inference endpoints.
- \BACKEND_URL\: The deployed URL of the FastAPI server (required on the frontend).

