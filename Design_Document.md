# DocuChat: AI-Powered Document Q&A System

## 1. Introduction
This document outlines the architectural design and technical decisions for the AI-Powered Document Q&A System. The system is designed to ingest unstructured PDF data, generate semantic embeddings, and leverage Large Language Models (LLMs) to answer natural language queries accurately while citing source material.

## 2. Live Demo
**Application URL:** https://doc2chat-ai.streamlit.app/

## 3. Architecture Overview
The system employs a deeply decoupled, dual-cloud microservices architecture to ensure scalability, fault tolerance, and separation of concerns.

- **Frontend (Streamlit):** Handles UI/UX, session management, and secure file transmission.
- **Backend (FastAPI):** Serves as the orchestration layer, handling REST API requests, data chunking, and prompt injection.
- **Vector Storage (Qdrant):** Manages high-dimensional semantic search and retrieval.
- **AI Inference (Groq & Hugging Face):** Offloads heavy tensor operations and LLM generation to optimized cloud endpoints.

## 4. Data Flow
1. **Ingestion:** PDF files are streamed in-memory via \multipart/form-data\ to the \/api/upload\ endpoint.
2. **Chunking:** \LlamaIndex\ parses the text using a \SentenceSplitter\ (1000 token chunk size, 200 token overlap) to preserve semantic boundaries.
3. **Embedding:** Chunks are sent to the Hugging Face Serverless Inference API (\ll-MiniLM-L6-v2\), which returns 384-dimensional vector embeddings.
4. **Storage:** Vectors and metadata are upserted into Qdrant using UUID v5 for deterministic ID generation.
5. **Retrieval & Generation:** User queries are embedded, searched against Qdrant using Cosine Similarity, and the top-K contexts are injected into a structured prompt for the Groq \compound\ LLM.

## 5. Technical Decisions & Trade-offs
- **Stateless Backend:** By moving vector processing to Hugging Face and LLM processing to Groq, the FastAPI backend remains entirely stateless. This allows it to run on heavily constrained environments (e.g., Render Free Tier 512MB RAM) without Out-Of-Memory (OOM) crashes.
- **Session-based UI Storage:** Instead of saving PDFs to the frontend server's disk (which causes privacy leaks across concurrent users), files are held in temporary \st.session_state\ and streamed directly to the backend.
- **Decoupled Repositories:** Separating the frontend and backend dependency requirements (\
equirements.txt\ vs \ackend-requirements.txt\) ensures minimal container sizes and prevents dependency conflicts between Streamlit and FastAPI.
