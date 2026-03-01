# app/services/llm.py
# This file defines a mock function to generate a response based on the predicted category, urgency, and retrieved documents.
# It constructs a template-based response that summarizes the classification results and relevant runbook

"""Mock LLM generation — no API key required."""

# This is a placeholder for where you would integrate with an actual LLM (e.g., OpenAI, Azure, etc.) 
# to generate a more dynamic response based on the classification and retrieved documents.
def generate_response(category: str, urgency: str, retrieved_docs: list[dict]) -> str:
    """Build a template-based response from classification + RAG results."""
    doc_summaries = ""
    for i, doc in enumerate(retrieved_docs, 1):
        source = doc.get("source", "unknown")
        snippet = doc.get("text", "")[:200]
        doc_summaries += f"\n  {i}. [{source}] {snippet}"

    if not doc_summaries:
        doc_summaries = "\n  No relevant runbook documents found."

    return (
        f"Ticket classified as **{category}** with **{urgency}** urgency.\n\n"
        f"Recommended actions based on relevant runbooks:{doc_summaries}\n\n"
        f"Please follow the referenced runbook steps. Escalate if the issue persists."
    )
