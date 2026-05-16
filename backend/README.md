# AI PDF Reader Backend

Production-oriented backend for an AI-powered document intelligence platform built using FastAPI, PostgreSQL, pgvector, Celery, Redis, and Retrieval-Augmented Generation (RAG).

This backend powers:

* AI-based PDF understanding
* Semantic search
* Context-aware chat
* Streaming AI responses
* Document embeddings
* Knowledge extraction workflows

---

# System Overview

The backend is designed as a scalable AI document processing platform.

## Core Capabilities

* PDF upload and storage
* Background document processing
* Text extraction and chunking
* Embedding generation
* Semantic retrieval using pgvector
* RAG-based AI chat
* Streaming responses using SSE
* User authentication
* Chat history persistence
* Extensible AI artifact system

  * summaries
  * notes
  * flashcards

---

# Architecture

```text
                ┌────────────────────┐
                │     Frontend UI    │
                │   Next.js Client   │
                └────────┬───────────┘
                         │
                         ▼
                ┌────────────────────┐
                │     FastAPI API    │
                └────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
 ┌────────────┐   ┌──────────────┐  ┌─────────────┐
 │ Auth Layer │   │ Document Svc │  │ Chat / RAG  │
 └────────────┘   └──────┬───────┘  └──────┬──────┘
                          │                 │
                          ▼                 │
                 ┌────────────────┐         │
                 │ Processing Svc │         │
                 └──────┬─────────┘         │
                        ▼                   ▼
                ┌───────────────┐   ┌──────────────┐
                │ PostgreSQL DB │   │ Groq LLM API │
                │ + pgvector    │   └──────────────┘
                └──────┬────────┘
                       ▼
                ┌───────────────┐
                │ Redis + Celery│
                └───────────────┘
```

---

# Tech Stack

| Layer           | Technology               |
| --------------- | ------------------------ |
| API Framework   | FastAPI                  |
| Database        | PostgreSQL               |
| Vector Storage  | pgvector                 |
| ORM             | SQLAlchemy               |
| Background Jobs | Celery                   |
| Queue Broker    | Redis                    |
| Embeddings      | Sentence Transformers    |
| LLM             | Groq (Llama 3.1)         |
| Authentication  | JWT                      |
| Streaming       | Server-Sent Events (SSE) |
| Migrations      | Alembic                  |
| Validation      | Pydantic                 |

---

# Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── logging_middleware.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── middleware/
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── document_chunk.py
│   │   ├── chat_message.py
│   │   ├── flashcard.py
│   │   ├── summary.py
│   │   └── note.py
│   │
│   ├── nlp/
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   └── vector_store.py
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   ├── context_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── processing_service.py
│   │   ├── search_service.py
│   │   ├── storage_service.py
│   │   └── upload_service.py
│   │
│   ├── storage/
│   │
│   ├── tasks/
│   │   ├── chat_tasks.py
│   │   └── document_tasks.py
│   │
│   └── worker/
│       └── celery_app.py
│
├── requirements.txt
├── alembic.ini
└── main.py
```

---

# Features

## 1. Authentication

Supports:

* user registration
* login
* JWT-based authentication
* protected endpoints

### Endpoints

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

---

## 2. PDF Upload

Supports:

* PDF upload
* local file storage
* async document processing
* status tracking

### Endpoint

```http
POST /api/v1/upload/upload
```

### Document States

```text
queued
processing
uploaded
failed
```

---

## 3. Background Processing Pipeline

Document ingestion pipeline:

```text
PDF Upload
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Store Embeddings
    ↓
Semantic Search Ready
```

Processing runs asynchronously using Celery workers.

---

## 4. Semantic Search

Uses pgvector cosine similarity search.

### Endpoint

```http
POST /api/v1/search/
```

### Example Query

```text
What does RBI say about AI regulation?
```

### Response Includes

* matching chunks
* similarity score
* chunk metadata
* page references

---

## 5. AI Chat (RAG)

Retrieval-Augmented Generation pipeline:

```text
User Question
    ↓
Generate Query Embedding
    ↓
Retrieve Similar Chunks
    ↓
Build Context
    ↓
Send to LLM
    ↓
Stream Response
```

### Endpoint

```http
POST /api/v1/chat/stream
```

### Features

* streaming responses
* contextual retrieval
* document-grounded answers
* source-aware responses
* chat history support

---

## 6. Streaming Responses (SSE)

Streaming is implemented using:

```text
text/event-stream
```

Frontend receives:

```json
{
  "type": "token",
  "content": "AI"
}
```

---

# Database Schema

## users

| Column          | Type      |
| --------------- | --------- |
| id              | Integer   |
| email           | String    |
| hashed_password | String    |
| full_name       | String    |
| is_active       | Boolean   |
| created_at      | Timestamp |

---

## documents

| Column     | Type      |
| ---------- | --------- |
| id         | Integer   |
| user_id    | Integer   |
| filename   | String    |
| file_path  | String    |
| status     | String    |
| created_at | Timestamp |

---

## document_chunks

| Column      | Type        |
| ----------- | ----------- |
| id          | Integer     |
| document_id | Integer     |
| content     | Text        |
| chunk_index | Integer     |
| page_number | Integer     |
| embedding   | Vector(384) |

---

## chat_messages

Stores:

* user queries
* AI responses
* session history

---

# Environment Variables

Create:

```text
.env
```

Example:

```env
APP_NAME=AI PDF Reader
API_V1_PREFIX=/api/v1

POSTGRES_SERVER=localhost
POSTGRES_PORT=5433
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456789
POSTGRES_DB=ai_pdf_df

DATABASE_URL=postgresql+psycopg2://postgres:123456789@localhost:5433/ai_pdf_df

REDIS_URL=redis://localhost:6379/0

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

GROQ_API_KEY=your_groq_api_key
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repo-url>
cd backend
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Docker Setup

## PostgreSQL + pgvector

```bash
docker run -d \
  --name ai_pdf_pg \
  -e POSTGRES_PASSWORD=123456789 \
  -e POSTGRES_DB=ai_pdf_df \
  -p 5433:5432 \
  ankane/pgvector
```

---

## Redis

```bash
docker run -d \
  --name ai_pdf_redis \
  -p 6379:6379 \
  redis:7
```

---

# Database Setup

## Run Migrations

```bash
alembic upgrade head
```

---

# Running the Backend

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Running Celery Worker

## Windows

```bash
celery -A app.worker.celery_app worker --pool=solo --loglevel=info
```

## Linux/macOS

```bash
celery -A app.worker.celery_app worker --loglevel=info
```

---

# API Endpoints

## Health

```http
GET /api/v1/health/
```

---

## Auth

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

---

## Upload

```http
POST /api/v1/upload/upload
```

---

## Search

```http
POST /api/v1/search/
```

---

## Chat

```http
POST /api/v1/chat/stream
```

---

# Semantic Search Example

```http
POST /api/v1/search/
```

Query Parameters:

```text
query=What is RBI AI?
document_id=1
```

Example Response:

```json
{
  "query": "What is RBI AI?",
  "document_id": 1,
  "total_results": 5,
  "results": [
    {
      "chunk_id": 216,
      "similarity": 0.56,
      "content": "..."
    }
  ]
}
```

---

# AI Chat Example

```http
POST /api/v1/chat/stream
```

Query Parameters:

```text
document_id=1
question=What does RBI say about AI regulation?
session_id=1
```

Streaming Response:

```text
data: {"type":"token","content":"RBI"}
```

---

# Current System Status

## Completed

* FastAPI backend
* PostgreSQL integration
* pgvector embeddings
* Redis queue
* Celery workers
* PDF upload
* Semantic retrieval
* RAG chat
* Streaming responses
* JWT authentication
* Chat history

---

## Planned

* Multi-document retrieval
* Advanced citation system
* OCR pipeline
* Analytics engine
* RBAC
* Team workspaces
* Audit logs
* Object storage (MinIO/S3)
* Qdrant migration
* Kubernetes deployment

---

# Production Engineering Notes

## Important Considerations

### 1. Background Processing

Large PDFs should never be processed inside API requests.

Always use:

* Celery
* worker queues
* async ingestion

---

### 2. Embedding Storage

Current implementation uses pgvector.

Future production upgrade path:

* Qdrant
* Milvus
* hybrid retrieval

---

### 3. Streaming

Frontend should consume:

```text
text/event-stream
```

using:

* EventSource
* fetch streaming reader

---

### 4. Security

Production deployment should include:

* HTTPS
* secure JWT handling
* rate limiting
* RBAC
* audit logs
* encrypted secrets

---

# Future Vision

This backend is evolving toward:

```text
AI-Powered Government Knowledge Infrastructure
```

Target capabilities:

* large-scale GR ingestion
* multilingual semantic retrieval
* policy intelligence
* AI-assisted governance workflows
* enterprise knowledge operations

---

# License

Internal project / proprietary implementation.

---

# Author

Ajay

AI Systems Engineering · RAG Systems · Enterprise AI Platforms
