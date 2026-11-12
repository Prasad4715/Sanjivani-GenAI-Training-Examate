# Day 4 — FastAPI Service, Smart Search and Data Analysis

## Project
ChalanCheck — Traffic Challan Assistant

## Objective
Build a FastAPI service for traffic challan records, implement intelligent record searching using TF-IDF and cosine similarity, and analyze the dataset using pandas.

## Assigned Tasks

**S1 — FastAPI Service**
- Create `app/main.py`.
- Implement `GET /health`.
- Implement `GET /records?limit=`.
- Implement `GET /records/{id}` with HTTP 404 for missing records.
- Implement `GET /search?q=`.
- Implement `POST /questions`.
- Add How to Run instructions to the main README.

**S2 — Data Analysis and Smart Search**
- Create `analysis/explore.py` to print three dataset facts using pandas.
- Create `app/smart_search.py` using TF-IDF and cosine similarity.
- Connect the smart search function to the `/search` API endpoint.
- Create the `week-1` Git tag.

## Implementation Files

| File | Purpose |
|---|---|
| `../../app/main.py` | FastAPI application and endpoints |
| `../../app/records.py` | Loads and retrieves JSON records |
| `../../app/smart_search.py` | TF-IDF and cosine similarity ranking |
| `../../analysis/explore.py` | Pandas data exploration |
| `../../data/records.json` | Legal records dataset |
| `../../README.md` | Main project documentation |
| `../../requirements.txt` | Python dependencies |

## How to Run

From the project root, activate the virtual environment and install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

Run data exploration in another terminal:

```powershell
python analysis/explore.py
```

Test smart search:

```powershell
python -c "from app.smart_search import smart_search; print([(r['section'], r['similarity_score']) for r in smart_search('alcohol')])"
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records?limit=5` | Retrieve a limited number of records |
| GET | `/records/185` | Retrieve Section 185 |
| GET | `/search?q=alcohol` | Rank relevant records |
| POST | `/questions` | Accept a user question |

The `/questions` endpoint currently accepts questions but does not generate answers.

## Verified Results

- `/health` returned `status: ok`.
- `/records?limit=5` returned five records from a dataset of 20.
- `/records/185` retrieved Section 185.
- A missing section returned the expected 404 error message.
- `/search?q=alcohol` returned Section 185 with a similarity score of approximately 0.1716.
- `/questions` accepted a sample question successfully.

## Pandas Analysis

The data exploration script printed:

1. Unique legal sections: **20**
2. Highest recorded first-offence fine: **₹20,000**
3. Records with non-null repeat-offence fines: **7**

These are statistics from the extracted dataset, not independent verification of legal penalties.

## GitHub Submission

- Branch: `main`
- Day 4 commit: `372d84d`
- Git tag: `week-1`
- Tag pushed successfully to GitHub.

Repository: https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate

## Outcome

Completed the Day 4 FastAPI service, smart search, and pandas analysis. The implementation was tested and pushed to GitHub.

## Status

Day 4 implementation and Git submission completed. Legal-data accuracy review remains a separate task.