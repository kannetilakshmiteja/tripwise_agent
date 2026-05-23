import os

try:
    from langchain_core.prompts import PromptTemplate
except Exception:
    PromptTemplate = None

try:
    from llm_config import llm
except Exception:
    llm = None


template = """
You are an AI travel support assistant.

User Query:
{query}

Detected Intent:
{intent}

Booking Details:
{booking}

Policy Information:
{policy}

Generate a professional customer-friendly travel support response.
"""


def generate_response(query, intent, booking, policy):
    if not os.getenv("OPENAI_API_KEY") or llm is None or PromptTemplate is None:
        return (
            f"Your request is related to {intent}. "
            f"Booking details: {booking}. "
            f"Policy: {policy}"
        )

    prompt_template = PromptTemplate(
        input_variables=["query", "intent", "booking", "policy"],
        template=template
    )

    final_prompt = prompt_template.format(
        query=query,
        intent=intent,
        booking=booking,
        policy=policy
    )

    response = llm.invoke(final_prompt)
    return response.content