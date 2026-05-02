# AI PDF Reader (RAG-Based Multi-User System)

## Overview

AI PDF Reader is a production-oriented backend system designed to enable intelligent interaction with PDF documents. It supports multi-user environments, document ingestion, processing, and lays the foundation for Retrieval-Augmented Generation (RAG).

This system is built with scalability, modularity, and real-world deployment in mind.

---

## Core Features

### Authentication & Multi-User

* User registration and login
* JWT-based authentication
* Protected API routes
* User-specific document ownership

### Document Management

* Upload PDF documents
* Store metadata in PostgreSQL
* Local storage abstraction (S3-ready)

### Processing Pipeline

* PDF parsing
* Text extraction
* Intelligent chunking
* Chunk storage for retrieval

### Database

* PostgreSQL (Dockerized)
* SQLAlchemy ORM
* Multi-user relational schema

### AI Infrastructure

* pgvector enabled database
* Ready for embeddings + semantic search
* Designed for RAG pipelines

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* Pydantic v2

### Database

* PostgreSQL (Docker)
* pgvector extension

### AI / NLP

* Custom chunking pipeline
* Embedding-ready architecture

### DevOps

* Docker
* Docker Compose

---

## Project Structure

backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── nlp/
│   ├── storage/
│   ├── tasks/
│   └── main.py
├── scripts/
├── tests/

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repo-url>
cd AI_pdf_POC
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Run PostgreSQL with pgvector

```bash
docker-compose up -d
```

---

### 4. Enable pgvector

```bash
docker exec -it ai_pdf_pg psql -U postgres -d ai_pdf_df
```

```sql
CREATE EXTENSION vector;
```

---

### 5. Configure Environment

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:123456789@localhost:5432/ai_pdf_df
SECRET_KEY=your_secret_key
```

---

### 6. Initialize Database

```bash
cd backend
python -m scripts.init_db
```

---

### 7. Run Application

```bash
uvicorn app.main:app --reload
```

---

## API Access

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Completed Milestones

* Multi-user authentication system
* Document upload pipeline
* PDF processing and chunking
* Database schema (users, documents, chunks)
* Dockerized PostgreSQL with pgvector

---

## Upcoming Features

* Embedding generation
* Vector similarity search
* RAG-based chat system
* Flashcards and notes generation
* Analytics dashboard

---

## Design Philosophy

* Modular architecture
* Production-first approach
* Scalable and extensible
* Separation of concerns (API, services, DB, NLP)

---

## Author

Ajay (AI PDF Reader Project)
