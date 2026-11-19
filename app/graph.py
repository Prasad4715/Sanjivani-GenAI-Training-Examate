
"""LangGraph workflow for ChalanCheck."""

from typing import Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from app.agent_loop import (
    detect_repeat_offence,
    extract_section_codes,
    select_tools,
)
from app.rag import ask_question
from app.tools import challan_total_calculator


class AgentState(TypedDict, total=False):
    question: str
    sections: list[str]
    repeat_offence: bool
    selected_tools: list[str]
    approval: bool
    calculator_result: dict[str, Any]
    rag_result: dict[str, Any]
    answer: str
    errors: list[str]
    history: list[dict[str, str]]


def route_node(state: AgentState) -> dict:
    """Choose tools and remember the current question."""

    question = state["question"]
    sections = extract_section_codes(question)

    # Use previous sections for follow-up questions
    # when the current question contains none.
    if not sections:
        for item in reversed(state.get("history", [])):
            previous_sections = extract_section_codes(
                item.get("question", "")
            )
            if previous_sections:
                sections = previous_sections
                break

    return {
        "sections": sections,
        "repeat_offence": detect_repeat_offence(question),
        "selected_tools": select_tools(question),
        "approval": False,
        "calculator_result": {},
        "rag_result": {},
        "answer": "",
        "errors": [],
    }


def choose_next_node(state: AgentState) -> str:
    """Decide which node runs after routing."""

    tools = state.get("selected_tools", [])

    if "calculator" in tools:
        return "approval"

    return "rag"


def approval_node(state: AgentState) -> dict:
    """Pause until the user approves the calculation."""

    if not state.get("sections"):
        return {
            "approval": False,
            "errors": ["No section codes available for calculation."],
        }

    decision = interrupt({
        "message": "Approve maximum fine calculation?",
        "sections": state["sections"],
        "repeat_offence": state.get(
            "repeat_offence", False
        ),
    })

    approved = (
        decision is True
        or (
            isinstance(decision, str)
            and decision.strip().lower()
            in {"yes", "approve", "approved"}
        )
    )

    return {"approval": approved}


def calculation_node(state: AgentState) -> dict:
    """Execute the fine calculator after approval."""

    if not state.get("approval", False):
        return {}

    try:
        result = challan_total_calculator(
            sections=state["sections"],
            repeat_offence=state.get(
                "repeat_offence", False
            ),
        )
        return {"calculator_result": result}

    except Exception as exc:
        return {
            "errors": state.get("errors", [])
            + [f"Calculator failed: {exc}"]
        }


def rag_node(state: AgentState) -> dict:
    """Retrieve legal explanations from the PDFs."""

    question = state["question"]

    try:
        result = ask_question(
            question=question,
            top_k=5,
        )
        return {"rag_result": result}

    except Exception as exc:
        return {
            "errors": state.get("errors", [])
            + [f"RAG failed: {exc}"]
        }


def finalize_node(state: AgentState) -> dict:
    """Combine results and update conversation history."""

    parts = []

    calculator = state.get("calculator_result", {})
    rag = state.get("rag_result", {})

    if calculator:
        total = calculator.get("total_maximum_fine")
        subtotal = calculator.get("known_fines_subtotal", 0)

        if total is not None:
            parts.append(
                f"Maximum recorded fine total: ₹{total:,}."
            )
        else:
            parts.append(
                "Complete total unavailable. "
                f"Known subtotal: ₹{subtotal:,}."
            )

        for item in calculator.get("fine_breakdown", []):
            fine = item.get("maximum_fine")
            amount = (
                f"₹{fine:,}"
                if fine is not None
                else "unknown"
            )
            parts.append(
                f"Section {item['section']}: {amount}"
            )

        for item in calculator.get(
            "non_money_consequences", []
        ):
            parts.append(
                f"Section {item['section']} additional action: "
                f"{item['action']}"
            )

        parts.append(calculator.get("note", ""))

    if rag:
        parts.append(rag.get("answer", ""))

    if state.get("selected_tools") == ["calculator"] \
            and not state.get("approval", False):
        parts.append(
            "Fine calculation was not approved."
        )

    errors = state.get("errors", [])

    if errors:
        parts.append("Errors: " + "; ".join(errors))

    if not parts:
        parts.append("I don't know")

    answer = "\n\n".join(
        part for part in parts if part
    )

    history = list(state.get("history", []))
    history.append({
        "question": state["question"],
        "answer": answer,
    })

    return {
        "answer": answer,
        "history": history[-10:],
    }


def after_approval(state: AgentState) -> str:
    if state.get("approval", False):
        return "calculate"
    if "rag" in state.get("selected_tools", []):
        return "rag"
    return "finalize"


def after_calculation(state: AgentState) -> str:
    if "rag" in state.get("selected_tools", []):
        return "rag"
    return "finalize"


builder = StateGraph(AgentState)

builder.add_node("route", route_node)
builder.add_node("approval", approval_node)
builder.add_node("calculate", calculation_node)
builder.add_node("rag", rag_node)
builder.add_node("finalize", finalize_node)

builder.add_edge(START, "route")

builder.add_conditional_edges(
    "route",
    choose_next_node,
    {
        "approval": "approval",
        "rag": "rag",
    },
)

builder.add_conditional_edges(
    "approval",
    after_approval,
    {
        "calculate": "calculate",
        "rag": "rag",
        "finalize": "finalize",
    },
)

builder.add_conditional_edges(
    "calculate",
    after_calculation,
    {
        "rag": "rag",
        "finalize": "finalize",
    },
)

builder.add_edge("rag", "finalize")
builder.add_edge("finalize", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)


def run_graph(
    question: str | None = None,
    session_id: str = "default",
    approve: bool | None = None,
) -> dict:
    """Start or resume a LangGraph conversation."""

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    if approve is not None:
        result = graph.invoke(
            Command(resume=approve),
            config=config,
        )
    else:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        result = graph.invoke(
            {"question": question},
            config=config,
        )

    snapshot = graph.get_state(config)

    pending = bool(snapshot.next)

    return {
        "session_id": session_id,
        "pending_approval": pending,
        "approval_request": (
            snapshot.tasks[0].interrupts[0].value
            if pending
            and snapshot.tasks
            and snapshot.tasks[0].interrupts
            else None
        ),
        "answer": (
            None if pending else result.get("answer")
        ),
        "sections": result.get("sections", []),
        "errors": result.get("errors", []),
        "history": result.get("history", []),
    }
