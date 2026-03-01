"""Mock LLM generation — no API key required."""


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
