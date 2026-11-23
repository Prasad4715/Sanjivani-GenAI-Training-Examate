# ChalanCheck — Interview Preparation

## 1. 60-Second Project Pitch

Good morning.

My project is ChalanCheck, an AI-powered Traffic Challan Assistant developed using Python, FastAPI, Streamlit, Google Gemini, Retrieval-Augmented Generation (RAG), ChromaDB, and LangGraph.

The main problem we solve is that many people receive traffic challans mentioning only a section number and fine amount, without understanding which traffic rule they violated.

ChalanCheck allows users to ask questions about traffic violations in simple language.

We collected four legal documents, including the Motor Vehicles Act, 1988, and its 2019 amendment. We processed these documents and created a searchable legal knowledge base.

When a user asks a question, our RAG pipeline retrieves relevant legal passages from ChromaDB. Google Gemini then generates an explanation supported by legal citations.

We also implemented LangGraph agent workflows, response caching, token usage tracking, and input validation.

Finally, we deployed the FastAPI backend and Streamlit frontend on Render using Docker.

The goal of ChalanCheck is to make traffic law information easier to understand while keeping answers grounded in official legal documents.

---

## 2. Hardest Problem Faced During Development

### Problem 1: Central Maximum Fines vs Maharashtra Compounding Amounts

One of the most challenging parts of ChalanCheck was handling differences between the maximum penalties provided under the Motor Vehicles Act and the amounts payable for compounding certain offences in Maharashtra.

The Motor Vehicles Act specifies statutory penalties, including maximum fines for certain offences.

However, Section 200 provides a mechanism under which specified offences may be compounded for amounts notified by the relevant government.

This means that a Maharashtra compounding amount may differ from the statutory maximum penalty under the Act.

For example, if the Act provides a maximum fine of ₹5,000 for a particular offence, we cannot automatically tell the user that their actual challan amount must be ₹5,000.

The notified compounding amount may be different, and not every offence is compoundable.

**Our solution:**

We designed ChalanCheck to distinguish between the statutory fine under the Act and the amount shown on an individual challan.

When explaining a penalty, the assistant should clearly identify it as the **maximum fine under the Act**, where applicable, rather than presenting it as the exact amount payable on the user's challan.

For an exact Maharashtra compounding amount, the system would need the applicable notification, offence details, and relevant date.

**What I learned:**

Legal AI systems must preserve the difference between statutory penalties, government-notified amounts, and case-specific enforcement decisions.

### Problem 2: Parsing Amended Legal PDFs

Another challenge was extracting accurate legal text from the consolidated Motor Vehicles Act PDF.

Some sections contain footnotes, amendment references, and struck-through or substituted provisions.

A basic PDF text extractor may capture both older and newer wording without clearly identifying which provision is currently applicable.

This can cause incorrect fine amounts or outdated legal explanations.

**Our approach:**

We used Python and PyMuPDF to extract legal text, applied cleaning and parsing logic, and organized the information into structured records.

We checked extracted section text and fine values against the legal source documents during development.

We also used RAG retrieval and source citations to help users trace answers back to the documents.

**What I learned:**

Extracting text from a legal PDF is not the same as correctly interpreting the current law. Amendment history, effective dates, and source verification are essential.

---

## 3. Ten Likely Interview Questions and Answers

### Q1. What is ChalanCheck?

ChalanCheck is an AI-powered traffic challan explanation system. It helps users understand traffic offences, Motor Vehicles Act sections, statutory fines, and possible additional legal consequences in simple language.

### Q2. Why did you choose this project?

Many people receive e-challans without understanding the legal section or reason for the penalty. We wanted to make legal information easier to access and understand through a conversational AI application.

### Q3. What technologies did you use?

We used Python for development, FastAPI for backend APIs, Streamlit for the frontend, Google Gemini for answer generation, Sentence Transformers for embeddings, ChromaDB for vector storage, LangGraph for agent workflows, Docker for containerization, GitHub Actions for CI/CD, and Render for deployment.

### Q4. What is RAG, and why did you use it?

RAG stands for Retrieval-Augmented Generation.

Instead of asking the LLM to answer only from its training knowledge, RAG first retrieves relevant information from our legal documents.

The retrieved information is then provided to Gemini so it can generate a more evidence-grounded answer.

We used RAG because legal answers should be supported by identifiable sources.

### Q5. How does your RAG pipeline work?

First, we extract text from legal PDFs and split it into smaller chunks.

Next, Sentence Transformers converts these chunks into numerical embeddings, which are stored in ChromaDB.

When a user asks a question, we create an embedding for the question and retrieve similar legal passages.

Finally, Gemini receives the retrieved context and generates an answer with source citations.

### Q6. Why did you use ChromaDB?

ChromaDB is a vector database that stores document embeddings and supports similarity search.

It helps our application retrieve legal passages related to the user's question, even when the question does not use exactly the same words as the document.

### Q7. Why did you use LangGraph?

LangGraph helps organize multi-step agent workflows.

In ChalanCheck, it supports tool execution, conversation state, and approval-based workflows for actions such as fine calculations.

This gives the application a structured way to manage operations beyond a single LLM response.

### Q8. How did you reduce hallucinations?

We used RAG to supply relevant legal passages, instructed Gemini to rely on the retrieved evidence, and included source citations in the response.

The system is also designed to say "I don't know" when the available evidence is insufficient.

However, citations and prompting reduce risk rather than guarantee complete factual accuracy.

### Q9. How did you improve performance and reliability?

We added request latency logging, Gemini token usage and estimated cost tracking, an in-memory response cache, and a 2,000-character question limit.

Our cache expires after 10 minutes and supports up to 100 entries.

We also tested a prompt-injection attempt and ran automated tests and Ruff code-quality checks.

### Q10. How did you deploy the project?

We containerized the application using Docker.

The FastAPI backend and Streamlit frontend were deployed as separate Render services.

We used GitHub Actions to automate code-quality checks, testing, and Docker build validation.

The application is accessible through public URLs, and the FastAPI endpoints can be explored using Swagger UI.

---

## 4. Project Links

**GitHub Repository:** https://github.com/Prasad4715/Sanjivani-GenAI-Training-Examate

**Live Application:** https://chalancheck-ui.onrender.com

**Backend API:** https://chalancheck-api.onrender.com

**API Documentation:** https://chalancheck-api.onrender.com/docs