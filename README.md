# ChalanCheck – Traffic Challan Assistant

## Project Overview

ChalanCheck is an AI-powered Traffic Challan Assistant designed to help Indian vehicle owners understand traffic violations and e-challans in simple language.

The application uses Python, FastAPI, Streamlit, Retrieval-Augmented Generation (RAG), Google Gemini, ChromaDB, and LangGraph to provide understandable explanations of traffic offences, penalties, and relevant legal provisions.

## Problem Statement

Many vehicle owners receive traffic challans containing Motor Vehicles Act section numbers and penalty amounts without understanding the actual offence or applicable legal provisions.

ChalanCheck aims to simplify this information and make traffic rules easier to understand.

## Target Users

Indian vehicle owners, particularly two-wheeler riders who want to understand their traffic challans.

## Key Features

- Explain Motor Vehicles Act sections in simple language.
- Display first and repeat offence penalties.
- Explain additional legal consequences, including imprisonment where applicable.
- Search traffic offences using TF-IDF and semantic search.
- Answer traffic law questions using RAG and Google Gemini.
- Retrieve relevant legal information from ChromaDB.
- Provide references to legal sources.
- Support an AI agent with tool calling and approval workflows.
- Calculate combined statutory fines for multiple sections.
- Provide a Streamlit-based user interface.
- Run the application using Docker Compose.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | Google Gemini |
| RAG | ChromaDB, Sentence Transformers |
| AI Agent | LangGraph |
| Search | TF-IDF, Cosine Similarity |
| Data Processing | Pandas, PyMuPDF |
| Testing | Pytest, Ruff |
| Containerization | Docker, Docker Compose |

## Data Sources

- Motor Vehicles Act, 1988
- Motor Vehicles (Amendment) Act, 2019
- Central Motor Vehicles Rules, 1989
- Maharashtra Motor Vehicles Rules, 1989

Official source: https://www.indiacode.nic.in/handle/123456789/1798

The application uses structured legal records stored in `data/records.json`.

## Project Information

- **Project:** ChalanCheck
- **Developer:** Prasad Rajesh Tribhuvan

## How to Run ChalanCheck Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate.git
cd Sanjivani-GenAI-Training-Examate
```

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit API keys or the `.env` file to GitHub.

### 5. Start FastAPI

```powershell
python -m uvicorn app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 6. Start Streamlit

Open another terminal in the project root:

```powershell
python -m streamlit run ui/app.py
```

Streamlit application: http://localhost:8501

## Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records` | Retrieve legal records |
| GET | `/records/{id}` | Retrieve a record by section |
| GET | `/search?q=alcohol` | Search traffic offences |
| GET | `/search/semantic` | Semantic search |
| POST | `/questions` | Submit a question |
| POST | `/ask` | Generate a RAG-based answer |
| POST | `/agent` | Execute the AI agent workflow |

## Run with Docker

Docker Compose allows the FastAPI backend and Streamlit frontend to run together in separate containers.

### Prerequisites

- Docker Desktop installed and running
- Docker Compose
- Gemini API key for AI-powered responses

### 1. Clone the Repository

```bash
git clone https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate.git
cd Sanjivani-GenAI-Training-Examate
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Build and Start Containers

```powershell
docker compose up --build -d
```

This starts two services:

- **API:** FastAPI backend on port 8000
- **UI:** Streamlit frontend on port 8501

### 4. Access the Application

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| FastAPI Documentation | http://localhost:8000/docs |
| API Health Check | http://localhost:8000/health |

### 5. Check Container Status

```powershell
docker compose ps
```

### 6. View Container Logs

```powershell
docker compose logs -f
```

### 7. Stop Containers

```powershell
docker compose down
```

### Docker Configuration

- `Dockerfile` defines the application image.
- `.dockerignore` excludes unnecessary local files and secrets.
- `docker-compose.yml` configures the API and UI services.
- Streamlit communicates with FastAPI using `http://api:8000` inside Docker.
- The local `data/` directory is mounted into both containers to preserve application data.

## Testing and Code Quality

Run automated tests:

```powershell
python -m pytest tests/ -q
```

Check code quality:

```powershell
python -m ruff check .
```

The project includes automated tests for legal records, search functionality, API endpoints, mocked LLM responses, and agent tools.

## Additional Development Commands

### Data Exploration

```powershell
python analysis/explore.py
```

### Test Smart Search

```powershell
python -c "from app.smart_search import smart_search; print([(r['section'], r['similarity_score']) for r in smart_search('alcohol')])"
```

## Disclaimer

ChalanCheck is intended for educational and informational purposes. Legal provisions, penalties, and enforcement practices may change. Users should verify important information against current official legal sources. The application does not replace professional legal advice.