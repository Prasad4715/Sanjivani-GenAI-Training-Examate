# ChalanCheck – Traffic Challan Assistant

## Project Overview
ChalanCheck is an AI-powered Traffic Challan Assistant designed to help Indian vehicle owners understand traffic violations and e-challans in simple language.

## Problem Statement
Many vehicle owners receive traffic challans containing Motor Vehicles Act section numbers and penalty amounts without understanding the actual offence or applicable legal provisions.

ChalanCheck aims to simplify this information and make traffic rules easier to understand.

## Target Users
Indian vehicle owners, particularly two-wheeler riders who want to understand their traffic challans.

## Key Features (Planned)
- Understand Motor Vehicles Act sections.
- Explain traffic offences in simple language.
- Display applicable first and repeat offence penalties.
- Explain additional legal consequences.
- Decode challan text containing multiple section numbers.
- Provide references to official legal sources.

## Data Source
India Code – Motor Vehicles Act, 1988

https://www.indiacode.nic.in/handle/123456789/1798

## Project Information
- **Project:** ChalanCheck
- **Developer:** Prasad Rajesh Tribhuvan



## How to Run ChalanCheck

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

### 4. Start the FastAPI Server

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

### 5. Available API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check API health |
| GET | /records?limit=5 | Retrieve traffic challan records |
| GET | /records/{id} | Retrieve a record by section number |
| GET | /search?q=alcohol | Search records using TF-IDF and cosine similarity |
| POST | /questions | Submit a question (answer generation not yet implemented) |

### 6. Run Data Exploration

Open another terminal in the project root and run:

```powershell
python analysis/explore.py
```

This prints three facts about the ChalanCheck dataset using pandas.

### 7. Test Smart Search

```powershell
python -c "from app.smart_search import smart_search; print([(r['section'], r['similarity_score']) for r in smart_search('alcohol')])"
```

### Data Source

The application reads structured legal records from `data/records.json`, generated from the Motor Vehicles Act documents.

The records are intended for educational assistance and require legal accuracy verification before use as authoritative guidance.
