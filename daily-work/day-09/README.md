# Day 9 — Tool Calling and LangGraph Agent

## Project: ChalanCheck

### Objective

Implement a tool-calling agent that can explain traffic challans, calculate maximum recorded fines, maintain conversation context, and request user approval before performing calculations.

## Session 1 — Custom Tools and Hand-Written Agent

### 1. Challan Total Calculator

**File:** `app/tools.py`

Implemented `challan_total_calculator()` to calculate the combined maximum recorded fines for multiple Motor Vehicles Act sections.

Features:
- Accepts a list of section codes.
- Supports first and repeat offences.
- Retrieves fine information from `data/records.json`.
- Returns section-wise fine breakdowns.
- Includes additional non-monetary consequences.
- Identifies missing fine values without treating them as zero.
- Distinguishes recorded statutory maximum fines from actual payable challan amounts.

### 2. Hand-Written Agent

**File:** `app/agent_loop.py`

Implemented a rule-based tool-calling agent.

The agent:
- Identifies section numbers from user questions.
- Detects repeat-offence requests.
- Selects RAG, calculator, or both tools.
- Executes the selected tools.
- Combines results into a structured response.
- Handles tool errors and limits tool calls.

### 3. Session 1 Testing

Verified the following:

- Sections 180 and 181 returned a combined maximum recorded fine of ₹10,000.
- RAG successfully explained Section 194D with legal PDF citations.
- Combined calculator and RAG execution worked successfully.
- No errors occurred during the successful tests.

## Session 2 — LangGraph Agent

### 1. LangGraph Workflow

**File:** `app/graph.py`

Implemented a LangGraph workflow using:

- `StateGraph` for defining workflow nodes.
- `MemorySaver` for in-memory conversation state.
- `interrupt()` for pausing before calculations.
- `Command(resume=...)` for approval and rejection.

Workflow nodes:

1. Route
2. Approval
3. Calculate
4. RAG
5. Finalize

### 2. Conversation Memory

Implemented session-based conversation memory.

The agent remembers previously mentioned section numbers and uses them when answering follow-up calculation questions.

Verified that a follow-up question correctly reused Sections 180 and 181 and returned ₹10,000.

Memory currently lasts only while the application process is running.

### 3. Human-in-the-Loop Approval

Implemented an approval mechanism before fine calculations.

- Approval allows the calculation to proceed.
- Rejection prevents the calculation.
- Both outcomes are recorded in conversation history.

### 4. FastAPI Integration

**File:** `app/main.py`

Added:

`POST /agent`

The endpoint supports:

- New questions.
- Session IDs.
- Approval requests.
- Approval and rejection decisions.
- Final answers and conversation history.
- Request validation and error handling.

Existing API endpoints were preserved.

## Testing and Results

| Test | Result |
|---|---|
| Calculator tool | Passed |
| RAG tool | Passed |
| Combined tool execution | Passed |
| LangGraph compilation | Passed |
| Approval workflow | Passed |
| Rejection workflow | Passed |
| Conversation memory | Passed |
| FastAPI endpoint registration | Passed |
| API approval request | Passed |
| API approval completion | Passed |
| API rejection | Passed |

## Challenges and Fixes

**Circular import:** Resolved a circular import between `app/graph.py` and `app/agent_loop.py`.

**Repeat-offence detection:** Fixed incorrect detection of the word "again" as a repeat traffic offence.

**Missing fine information:** Kept missing fine values explicitly unknown instead of assuming zero.

## Limitations

- Fine calculations depend on the accuracy and completeness of `data/records.json`.
- The calculator reports sums of recorded statutory maximum fines, not official payable challan amounts.
- Tool selection uses predefined rules and may not recognize every phrasing.
- Conversation memory is stored in RAM and is lost after an application restart.
- Legal explanations require source verification.

## Outcome

Successfully developed and tested a ChalanCheck agent integrating custom calculation tools, retrieval-augmented legal explanations, LangGraph workflow management, conversation memory, human approval, and FastAPI integration.