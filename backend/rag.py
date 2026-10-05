import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# Knowledge Base Configuration
# ============================================================

KNOWLEDGE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "knowledge_base",
    "programming_knowledge.txt"
)


# ============================================================
# Load Knowledge Base
# ============================================================

def load_documents():

    if not os.path.exists(KNOWLEDGE_FILE):
        return []

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    # Split knowledge into sections
    documents = re.split(
        r"\n\s*\n",
        text
    )

    documents = [
        doc.strip()
        for doc in documents
        if doc.strip()
    ]

    return documents


# ============================================================
# Retrieve Relevant Documents
# ============================================================

def retrieve_context(
    query,
    task,
    top_k=3
):

    documents = load_documents()

    if not documents:
        return "No additional knowledge was found."

    search_query = f"{task} {query}"

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        document_vectors = vectorizer.fit_transform(
            documents
        )

        query_vector = vectorizer.transform(
            [search_query]
        )

        similarities = cosine_similarity(
            query_vector,
            document_vectors
        )[0]

        ranked_indices = similarities.argsort()[::-1]

        selected = []

        for index in ranked_indices[:top_k]:

            if similarities[index] > 0:

                selected.append(
                    documents[index]
                )

        if not selected:

            return "No highly relevant knowledge was found."

        return "\n\n---\n\n".join(selected)

    except Exception:

        return "Knowledge retrieval was unavailable."
