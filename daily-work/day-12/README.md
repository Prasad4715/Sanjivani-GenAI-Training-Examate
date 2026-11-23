# Day 12 – CI/CD and Cloud Deployment

## Objective
Set up automated GitHub Actions checks, merge a feature-branch pull request after successful CI, deploy the ChalanCheck FastAPI backend publicly, and verify the `/health` endpoint.

## Session 1 – GitHub Actions CI/CD

### Requirements
- Create `.github/workflows/ci.yml` to run Ruff, Pytest, and Docker build.
- Add a green CI badge to the main project README.
- Merge one feature-branch pull request only after CI checks pass.

### Work completed
1. Created and worked on branch `feature/day12-ci-deployment`.
2. Added the workflow file `.github/workflows/ci.yml`.
3. Configured the workflow to install project dependencies, run Ruff and Pytest, and build the Docker image.
4. Fixed missing dependency issues discovered in early CI runs.
5. Verified successful CI checks on push and pull request.
6. Added the GitHub Actions status badge to the root `README.md`.
7. Merged **Pull Request #1** into `main` after the checks passed.
8. Updated the local `main` branch.

### CI badge

[![ChalanCheck CI](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml/badge.svg)](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml)

### Evidence links
- [GitHub Actions workflow](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/actions/workflows/ci.yml)
- [Merged Pull Request #1](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate/pull/1)
- [Project repository](https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate)

## Session 2 – Render Deployment

### Requirements
- Deploy ChalanCheck using Render or Hugging Face Spaces.
- Add the public deployment URL to the main README and Excel tracker.
- Verify the `/health` endpoint publicly.

### Work completed
1. Updated the Dockerfile to respect the `PORT` environment variable used by the hosting platform.
2. Committed and pushed the Dockerfile changes to `main`.
3. Connected the GitHub repository to Render.
4. Created a Docker-based web service named `chalancheck-api` on Render's Free plan.
5. Configured `GEMINI_API_KEY` securely as a Render environment variable (the key is not stored in this document).
6. Deployed the FastAPI backend successfully.
7. Verified the public health endpoint returned `{"status":"ok"}`.
8. Confirmed the Swagger API documentation and legal records endpoint opened successfully.
9. Tested the `/chat` endpoint with a question about Section 185 of the Motor Vehicles Act. The endpoint returned an explanation, fine details, a confidence value, and a follow-up question.
10. Added the live API links to the main project README and recorded the deployment URL in the Excel tracker.

### Public deployment links

| Resource | URL |
|---|---|
| Live FastAPI backend | https://chalancheck-api.onrender.com |
| Public health endpoint | https://chalancheck-api.onrender.com/health |
| Swagger API documentation | https://chalancheck-api.onrender.com/docs |
| Legal records test | https://chalancheck-api.onrender.com/records?limit=2 |

### Health verification

**Request:** `GET https://chalancheck-api.onrender.com/health`

**Verified response:**

```json
{"status":"ok"}
```

### AI functionality test

**Endpoint:** `POST /chat`

**Request:**

```json
{
  "question": "Explain Section 185 of the Motor Vehicles Act in simple words.",
  "prompt_version": "v2"
}
```

**Observed result:** A structured answer explaining Section 185, first and repeat offence fine information, additional legal action, and a disclaimer. The JSON response included `answer`, `confidence`, and `follow_up` fields.

## Deliverables and Final Status

| Requirement | Result |
|---|---|
| Ruff, Pytest and Docker build in GitHub Actions | Completed; CI passed |
| CI badge in root README | Completed |
| Feature-branch PR merged after green CI | Completed |
| FastAPI backend deployed on Render | Completed |
| Public `/health` verified | Completed |
| Live URL in root README | Completed |
| Live URL in Excel tracker | Completed |
| Swagger UI and legal records endpoints | Verified |
| Gemini chat response | Verified with Section 185 question |

## Important Notes
- **Publicly deployed:** FastAPI backend only. The Streamlit frontend was running locally and was not deployed as part of this Render service.
- Render Free instances may spin down after inactivity, so the first request can be delayed.
- A passing `/health` endpoint confirms that the API process responds; it does not guarantee that every AI or retrieval workflow works in all cases.
- Never commit `.env` files or API keys.

## Outcome
**Day 12 completed according to the specified S1 and S2 requirements.** The public backend is live, CI checks passed, the feature PR was merged, and the deployment URL was documented in the README and Excel tracker.
