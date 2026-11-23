# ChalanCheck – Traffic Challan Assistant

[![ChalanCheck CI](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml/badge.svg)](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml)

**AI-Powered Traffic Challan Explanation System | FastAPI | Streamlit | Google Gemini | RAG | LangGraph | Docker**

## Live Deployment

The ChalanCheck FastAPI backend is deployed on Render using Docker.

| Service | Link |
|---|---|
| Live FastAPI Backend | [ChalanCheck API](https://chalancheck-api.onrender.com) |
| Public Health Check | [Check API Health](https://chalancheck-api.onrender.com/health) |
| Interactive API Documentation | [Swagger UI](https://chalancheck-api.onrender.com/docs) |
| CI/CD Pipeline | [GitHub Actions](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml) |
| Source Code | [GitHub Repository](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate) |

**Deployment Platform:** Render  
**Deployment Method:** Docker  
**Backend Status:** Successfully deployed  
**Health Check:** Verified publicly with `{"status":"ok"}`  
**Frontend:** Streamlit (available locally through Python or Docker Compose)

> **Note:** Render's Free instance may spin down after inactivity. The first request after a period of inactivity can take longer than usual.

## Project Overview

ChalanCheck is an AI-powered Traffic Challan Assistant designed to help Indian vehicle owners understand traffic violations and e-challans in simple language.

The application uses Python, FastAPI, Streamlit, Retrieval-Augmented Generation (RAG), Google Gemini, ChromaDB, and LangGraph to explain traffic offences, penalties, and relevant legal provisions.

It combines structured legal records, keyword-based search, semantic retrieval, and AI-generated responses to make traffic law information easier to understand.

## Problem Statement

Many vehicle owners receive traffic challans containing Motor Vehicles Act section numbers and penalty amounts without clearly understanding the offence or its legal consequences.

For example, a two-wheeler rider may receive an e-challan SMS mentioning only a section number and fine amount.

ChalanCheck helps users understand:

- Which traffic rule was violated.
- What the relevant Motor Vehicles Act section means.
- The applicable first and repeat offence penalties.
- Whether additional legal consequences may apply.
- Which legal sources support the explanation.

## Target Users

Indian vehicle owners, particularly two-wheeler riders who want to understand their traffic challans and related legal provisions.

## Key Features

- **Traffic Challan Explanation:** Explain Motor Vehicles Act sections in simple language.
- **Penalty Information:** Display first and repeat offence penalties from structured legal records.
- **Additional Legal Consequences:** Explain imprisonment and other actions where applicable.
- **Keyword Search:** Search traffic offences using TF-IDF and cosine similarity.
- **Semantic Search:** Retrieve relevant legal information using Sentence Transformers and ChromaDB.
- **RAG-Based Question Answering:** Generate answers grounded in retrieved legal documents using Google Gemini.
- **Legal Citations:** Provide references to relevant legal documents.
- **AI Agent:** Use LangGraph for agent workflows, tool execution, and approval handling.
- **Fine Calculation:** Calculate combined statutory fine amounts for multiple sections.
- **Web Interface:** Interact with the application through Streamlit.
- **REST API:** Access application functionality through FastAPI endpoints.
- **Docker Support:** Run the backend and frontend using Docker Compose.
- **CI/CD:** Automatically run code-quality checks, tests, and Docker builds through GitHub Actions.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Large Language Model | Google Gemini |
| RAG | ChromaDB, Sentence Transformers |
| AI Agent | LangGraph |
| Search | TF-IDF, Cosine Similarity |
| Data Processing | Pandas, PyMuPDF |
| Testing | Pytest |
| Code Quality | Ruff |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud Deployment | Render |
| Version Control | Git, GitHub |

## Data Sources

ChalanCheck uses legal information from the following documents:

1. Motor Vehicles Act, 1988
2. Motor Vehicles (Amendment) Act, 2019
3. Central Motor Vehicles Rules, 1989
4. Maharashtra Motor Vehicles Rules, 1989

**Official Legal Source:** [India Code – Motor Vehicles Act](https://www.indiacode.nic.in/handle/123456789/1798)

The application stores structured legal records in `data/records.json`.

These records contain information such as section numbers, offence descriptions, first and repeat offence fines, additional actions, and source references.

## Application Workflow

ChalanCheck supports structured legal searches and AI-powered question answering.

**RAG Question-Answering Workflow:**

1. The user submits a traffic challan question.
2. FastAPI receives and validates the request.
3. The application searches the legal knowledge base.
4. ChromaDB retrieves relevant legal document chunks using semantic search.
5. The retrieved information is passed to Google Gemini.
6. Gemini generates an explanation based on the available legal context.
7. The API returns the answer with relevant legal citations.

**AI Agent Workflow:**

The LangGraph agent manages questions, tool execution, conversation state, and approval-based fine calculations.

## Project Information

- **Project:** ChalanCheck
- **Developer:** Prasad Rajesh Tribhuvan
- **Category:** Generative AI / Citizen Services
- **Repository:** [Sanjivani-GenAI-Training-Examate](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate)

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

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own Gemini API key.

**Security:** Never commit API keys or the `.env` file to GitHub.

### 5. Start FastAPI

```powershell
python -m uvicorn app.main:app --reload
```

The backend runs locally at:

- API: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

### 6. Start Streamlit

Open another terminal in the project root:

```powershell
python -m streamlit run ui/app.py
```

Open the Streamlit application:

http://localhost:8501

## Available API Endpoints

The following endpoints are defined in the FastAPI application.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records` | Retrieve legal records |
| GET | `/records/{id}` | Retrieve a record by section number |
| GET | `/search?q=alcohol` | Search traffic offences using TF-IDF |
| GET | `/search/semantic?q=helmet` | Perform semantic search |
| POST | `/questions` | Submit a question |
| POST | `/chat` | Generate a Gemini-based challan explanation |
| POST | `/ask` | Generate a RAG-based answer with citations |
| POST | `/agent` | Execute the LangGraph agent workflow |

### Public API Documentation

The deployed API provides interactive Swagger documentation:

https://chalancheck-api.onrender.com/docs

The public `/health` endpoint has been verified. Other endpoints depend on their respective data, model, and API configurations.

## Run with Docker

Docker Compose allows FastAPI and Streamlit to run in separate containers.

### Prerequisites

- Docker Desktop installed and running.
- Docker Compose.
- Gemini API key for AI-powered features.

### 1. Clone the Repository

```bash
git clone https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate.git
cd Sanjivani-GenAI-Training-Examate
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Build and Start Containers

```powershell
docker compose up --build -d
```

Docker Compose starts two services:

- **API:** FastAPI backend on port 8000.
- **UI:** Streamlit frontend on port 8501.

### 4. Access the Application

| Service | Local URL |
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

- `Dockerfile` defines the application image and startup command.
- `.dockerignore` excludes unnecessary local files and secrets.
- `docker-compose.yml` configures the API and UI services.
- Streamlit communicates with FastAPI through `http://api:8000` inside Docker.
- The local `data/` directory is mounted into both containers to preserve application data.

## CI/CD Pipeline

ChalanCheck uses GitHub Actions for automated code-quality checks, testing, and Docker image validation.

**Workflow File:** `.github/workflows/ci.yml`

The CI workflow performs three main checks:

1. **Ruff:** Checks Python code quality.
2. **Pytest:** Runs automated application tests.
3. **Docker Build:** Verifies that the Docker image builds successfully.

The workflow runs on configured GitHub push and pull-request events.

A feature-branch pull request was successfully merged into `main` after the CI checks passed.

**CI Status:**

[![ChalanCheck CI](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml/badge.svg)](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml)

**Workflow:** [View GitHub Actions](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml)

## Cloud Deployment

The FastAPI backend is deployed on Render using the project's Dockerfile.

### Deployment Configuration

| Setting | Value |
|---|---|
| Platform | Render |
| Service Name | `chalancheck-api` |
| Runtime | Docker |
| Git Branch | `main` |
| Dockerfile | `Dockerfile` |
| Environment Variable | `GEMINI_API_KEY` |
| Deployment URL | https://chalancheck-api.onrender.com |

The Dockerfile starts Uvicorn on Render's configured port, defaulting to port 8000 when the `PORT` environment variable is not set.

### Public Health Check

**URL:** https://chalancheck-api.onrender.com/health

**Verified Response:**

```json
{
  "status": "ok"
}
```

This confirms that the deployed FastAPI application responds successfully to health-check requests.

The public Streamlit frontend is not part of this Render backend service. It can currently be run locally using Python or Docker Compose.

## Testing and Code Quality

### Run Automated Tests

```powershell
python -m pytest tests/ -q
```

### Check Code Quality

```powershell
python -m ruff check .
```

The project includes tests covering legal records, search functionality, API endpoints, mocked LLM responses, and agent tools.

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

ChalanCheck is intended for educational and informational purposes only.

Traffic laws, penalties, and enforcement practices may change. Users should verify important legal information against current official government sources.

The application does not replace professional legal advice.