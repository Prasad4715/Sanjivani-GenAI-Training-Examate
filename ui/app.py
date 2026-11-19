
import json
import os
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path

import requests
import streamlit as st

# --------------------------------------------------
# Configuration
# --------------------------------------------------
API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_FILE = PROJECT_ROOT / "data" / "chat_feedback.jsonl"

st.set_page_config(
    page_title="ChalanCheck",
    page_icon="🚦",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = False

if "approval_request" not in st.session_state:
    st.session_state.approval_request = None

if "decoder_result" not in st.session_state:
    st.session_state.decoder_result = None


# --------------------------------------------------
# Backend API functions
# --------------------------------------------------

def ask_backend(question: str) -> dict:
    """Ask the RAG endpoint for a legal explanation."""
    response = requests.post(
        f"{API_URL}/ask",
        json={
            "question": question,
            "top_k": 5,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def agent_backend(
    question: str | None = None,
    approve: bool | None = None,
) -> dict:
    """Call the LangGraph agent endpoint."""
    payload = {
        "session_id": st.session_state.session_id,
    }

    if approve is not None:
        payload["approve"] = approve
    elif question is not None:
        payload["question"] = question
    else:
        raise ValueError("Question or approval is required.")

    response = requests.post(
        f"{API_URL}/agent",
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def get_record(section: str) -> dict | None:
    """Retrieve one section directly, avoiding pagination."""
    response = requests.get(
        f"{API_URL}/records/{section}",
        timeout=15,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()


# --------------------------------------------------
# Feedback storage
# --------------------------------------------------

def save_feedback(
    question: str,
    answer: str,
    rating: str,
    message_id: str,
) -> None:
    """Append one feedback event to a local JSONL file."""
    if rating not in {"up", "down"}:
        raise ValueError("Invalid feedback rating.")

    FEEDBACK_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    feedback = {
        "timestamp": datetime.now(UTC).isoformat(),
        "session_id": st.session_state.session_id,
        "message_id": message_id,
        "question": question,
        "answer": answer,
        "rating": rating,
    }

    with FEEDBACK_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(feedback, ensure_ascii=False) + "\n"
        )


# --------------------------------------------------
# Chat helpers
# --------------------------------------------------

def add_message(
    role: str,
    content: str,
    citations: list | None = None,
    question: str = "",
) -> None:
    st.session_state.messages.append(
        {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "citations": citations or [],
            "question": question,
            "feedback": None,
        }
    )


def display_citations(citations: list) -> None:
    """Display citations returned by the RAG endpoint."""
    if not citations:
        st.caption("No legal citations returned.")
        return

    with st.expander(f"📚 Legal sources ({len(citations)})"):
        for citation in citations:
            reference = citation.get("reference", "Unknown")
            title = citation.get("title", "Legal document")
            source = citation.get("source", "Unknown")
            page = citation.get("page", "Unknown")

            st.markdown(f"**{reference} — {title}**")
            st.write(f"Source: {source}")
            st.write(f"Page: {page}")
            st.divider()


def display_feedback(message: dict) -> None:
    """Show feedback controls for an assistant response."""
    if message.get("feedback"):
        rating = message["feedback"]
        label = "👍 Helpful" if rating == "up" else "👎 Not helpful"
        st.caption(f"Feedback saved: {label}")
        return

    message_id = message["id"]

    col1, col2, _ = st.columns([1, 1, 5])

    with col1:
        up = st.button(
            "👍",
            key=f"up_{message_id}",
            help="Helpful",
        )

    with col2:
        down = st.button(
            "👎",
            key=f"down_{message_id}",
            help="Not helpful",
        )

    if up or down:
        rating = "up" if up else "down"

        try:
            save_feedback(
                question=message.get("question", ""),
                answer=message["content"],
                rating=rating,
                message_id=message_id,
            )

            message["feedback"] = rating
            st.rerun()

        except OSError as error:
            st.error(f"Could not save feedback: {error}")


def render_chat_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                display_citations(
                    message.get("citations", [])
                )
                display_feedback(message)


# --------------------------------------------------
# Agent approval handling
# --------------------------------------------------

def process_agent_result(
    result: dict,
    original_question: str = "",
) -> None:
    """Update the UI from the LangGraph agent response."""
    pending = result.get("pending_approval", False)

    st.session_state.pending_approval = pending
    st.session_state.approval_request = (
        result.get("approval_request") if pending else None
    )

    if pending:
        return

    answer = result.get("answer") or "No answer was returned."

    errors = result.get("errors", [])
    if errors:
        answer += "\n\n**Agent errors:** " + "; ".join(errors)

    add_message(
        role="assistant",
        content=answer,
        question=original_question,
    )


def display_approval_controls() -> None:
    if not st.session_state.pending_approval:
        return

    approval = st.session_state.approval_request or {}

    with st.container(border=True):
        st.subheader("✋ Calculation Approval Required")
        st.write(
            approval.get(
                "message",
                "Approve maximum fine calculation?",
            )
        )

        sections = approval.get("sections", [])
        st.write(f"**Sections:** {', '.join(sections)}")

        st.write(
            "**Offence type:** "
            + (
                "Repeat offence"
                if approval.get("repeat_offence")
                else "First offence"
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            approve_clicked = st.button(
                "✅ Approve",
                type="primary",
                use_container_width=True,
            )

        with col2:
            reject_clicked = st.button(
                "❌ Reject",
                use_container_width=True,
            )

        if approve_clicked or reject_clicked:
            try:
                result = agent_backend(
                    approve=approve_clicked,
                )

                # The latest user message is the pending question.
                question = next(
                    (
                        msg["content"]
                        for msg in reversed(st.session_state.messages)
                        if msg["role"] == "user"
                    ),
                    "",
                )

                process_agent_result(result, question)
                st.rerun()

            except requests.exceptions.RequestException as error:
                st.error(
                    "Could not resume the agent. "
                    "Please check the backend."
                )
                st.caption(str(error))


# --------------------------------------------------
# Challan Decoder helpers
# --------------------------------------------------

def extract_challan_sections(text: str) -> list[str]:
    """Extract section codes from a simple challan format."""
    prefix = re.split(
        r"\b(?:MVA|MV ACT|MOTOR VEHICLES ACT)\b"
        r"|₹"
        r"|\bRS\.?\s*\d",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    matches = re.findall(
        r"(?<![A-Za-z0-9])\d{1,3}[A-Za-z]?"
        r"(?![A-Za-z0-9])",
        prefix,
    )

    return list(
        dict.fromkeys(code.upper() for code in matches)
    )


def format_fine(value) -> str:
    if value is None:
        return "Not specified in current records"

    try:
        return f"₹{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def decode_challan(text: str, is_repeat: bool) -> dict:
    """Fetch section-wise legal information for a challan."""
    sections = extract_challan_sections(text)

    amount_match = re.search(
        r"₹\s*([\d,]+)",
        text,
    )

    amount = (
        amount_match.group(1)
        if amount_match
        else None
    )

    cards = []

    for section in sections:
        try:
            record = get_record(section)

            cards.append(
                {
                    "section": section,
                    "record": record,
                    "error": None,
                }
            )

        except (requests.exceptions.RequestException, ValueError) as error:
            cards.append(
                {
                    "section": section,
                    "record": None,
                    "error": str(error),
                }
            )

    return {
        "sections": sections,
        "amount": amount,
        "repeat_offence": is_repeat,
        "cards": cards,
    }


def display_decoder_result(result: dict) -> None:
    sections = result.get("sections", [])

    if not sections:
        st.warning("No section numbers were found.")
        return

    st.write(f"**Detected sections:** {', '.join(sections)}")

    amount = result.get("amount")

    if amount:
        st.info(
            f"Challan amount mentioned: ₹{amount}. "
            "This may differ from the statutory maximum fine."
        )

    is_repeat = result.get("repeat_offence", False)

    for item in result.get("cards", []):
        section = item["section"]
        record = item.get("record")

        with st.container(border=True):
            st.markdown(f"### Section {section}")

            if item.get("error"):
                st.error(
                    f"Could not retrieve Section {section}."
                )
                st.caption(item["error"])
                continue

            if record is None:
                st.warning(
                    "This section is not available in the "
                    "current structured legal records."
                )
                continue

            st.write(
                f"**Offence:** "
                f"{record.get('offence') or 'Not specified'}"
            )

            st.write(
                "**Offence flag:** "
                + (
                    "Repeat offence"
                    if is_repeat
                    else "First offence"
                )
            )

            fine_field = (
                "max_fine_repeat"
                if is_repeat
                else "max_fine_first"
            )

            st.write(
                "**Maximum recorded fine:** "
                + format_fine(record.get(fine_field))
            )

            other_action = record.get("other_action")

            if other_action:
                st.write(
                    f"**Additional action:** {other_action}"
                )

            source_url = record.get("source_url")

            if (
                isinstance(source_url, str)
                and source_url.startswith(
                    ("https://", "http://")
                )
            ):
                st.link_button(
                    "📖 View Legal Source",
                    source_url,
                    key=f"source_{section}",
                )


# --------------------------------------------------
# Main UI
# --------------------------------------------------

st.title("🚦 ChalanCheck")
st.caption(
    "Understand Indian traffic challans using "
    "Motor Vehicles Act records and legal documents."
)

with st.sidebar:
    st.header("⚙️ Settings")

    chat_mode = st.radio(
        "Chat mode",
        options=[
            "Legal Q&A (RAG)",
            "AI Agent",
        ],
    )

    st.caption(
        "RAG provides legal explanations with PDF citations. "
        "AI Agent supports fine calculations and approval."
    )

    if st.button("🗑️ New Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.pending_approval = False
        st.session_state.approval_request = None
        st.rerun()

    st.divider()
    st.caption(
        "Legal information is for explanation only. "
        "Verify penalties with official sources."
    )


# --------------------------------------------------
# Chat interface
# --------------------------------------------------

st.subheader("💬 Ask About a Traffic Challan")

render_chat_history()

display_approval_controls()

question = st.chat_input(
    "Ask about a traffic challan or MVA section...",
    disabled=st.session_state.pending_approval,
)

if question:
    add_message("user", question)

    try:
        with st.spinner("Processing your question..."):
            if chat_mode == "Legal Q&A (RAG)":
                result = ask_backend(question)

                add_message(
                    role="assistant",
                    content=result.get(
                        "answer",
                        "No answer was returned.",
                    ),
                    citations=result.get("citations", []),
                    question=question,
                )

            else:
                result = agent_backend(question=question)
                process_agent_result(result, question)

        st.rerun()

    except requests.exceptions.RequestException as error:
        st.error(
            "Could not connect to ChalanCheck FastAPI. "
            "Make sure the backend is running."
        )
        st.caption(str(error))


# --------------------------------------------------
# Challan Decoder UI
# --------------------------------------------------

st.divider()
st.subheader("🧾 Challan Decoder")

st.caption(
    "Paste your challan text to see one card per "
    "detected Motor Vehicles Act section."
)

with st.form("decoder_form"):
    challan_text = st.text_area(
        "Challan text",
        placeholder="194D, 129/177 MVA ₹1000",
        height=100,
    )

    repeat_offence = st.checkbox(
        "This is a repeat traffic offence",
        value=False,
    )

    decode_clicked = st.form_submit_button(
        "🔍 Decode Challan",
        type="primary",
    )

if decode_clicked:
    if challan_text.strip():
        with st.spinner("Retrieving legal records..."):
            st.session_state.decoder_result = decode_challan(
                challan_text,
                repeat_offence,
            )
    else:
        st.session_state.decoder_result = None
        st.warning("Please paste your challan text first.")

if st.session_state.decoder_result is not None:
    display_decoder_result(
        st.session_state.decoder_result
    )

st.divider()
st.caption(
    "ChalanCheck | Statutory maximum fines are not "
    "necessarily the payable e-challan amount."
)
