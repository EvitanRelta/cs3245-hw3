# In the searching step, you will need to rank documents by cosine similarity
# based on tf×idf. In terms of SMART notation of ddd.qqq, you will need to
# implement the lnc.ltc ranking scheme (i.e., log tf and idf with cosine
# normalization for queries documents, and log tf, cosine normalization but
# no idf for documents. Compute cosine similarity between the query and each
# document, with the weights follow the tf×idf calculation, where term
# freq = 1 + log(tf) and inverse document frequency idf = log(N/df) (for queries).
# That is,

# tf-idf = (1 + log(tf)) * log(N/df).

import math
from collections import Counter
from typing import Any

from term_data import TermData


def get_log_tf(term_freq: int) -> float:
    """Computes logarithmic tf."""
    if term_freq == 0:
        return 0
    return 1 + math.log10(term_freq)


def get_tf_idf(term_freq: int, doc_freq: int, num_doc: int) -> float:
    """Computes TF-IDF."""
    return get_log_tf(term_freq) * math.log10(num_doc / doc_freq)


def get_norm_length(freq_dict: dict[Any, int]) -> float:
    """Get normalized length."""
    norm_length = 0
    for freq in freq_dict.values():
        norm_length += freq**2
    return math.sqrt(norm_length)


def get_dot_product(A: dict[Any, float], B: dict[Any, float]) -> float:
    """Computes the dot product between 2 sparse matrices A and B."""
    keys = set(A.keys()) | set(B.keys())
    return sum(A.get(key, 0) * B.get(key, 0) for key in keys)


def cosine_similarity(A: dict[Any, float], B: dict[Any, float]) -> float:
    """Computes the cosine similarity between 2 sparse matrices A and B."""
    A_norm: float = math.sqrt(sum(x**2 for x in A.values()))
    B_norm: float = math.sqrt(sum(x**2 for x in B.values()))
    if A_norm == 0 or B_norm == 0:
        return 0
    return get_dot_product(A, B) / (A_norm * B_norm)


def compute_query_weights(term_data_dict: dict[str, TermData]) -> dict[str, float]:
    query_weights: dict[str, float] = {}
    for term_data in term_data_list:
        query_weights[term_data.term] = get_tf_idf(
            query_terms.count(term), term_data.doc_freq, NUM_DOC
        )

    # Normalize query weights using cosine normalization
    norm: float = sqrt(sum(weight**2 for weight in query_weights.values()))
    if norm > 0:
        query_weights = {term: weight / norm for term, weight in query_weights.items()}

    return query_weights


def compute_doc_weights(doc_id: int, query_terms: list[str]) -> dict[str, float]:
    doc_weights: dict[str, float] = {}
    for term in query_terms:
        term_data: TermData = get_term_data(term)
        if doc_id in term_data.term_freq_dict:
            doc_weights[term] = 1 + math.log10(term_data.term_freq_dict[doc_id])

    # Normalize document weights using cosine normalization
    norm: float = sqrt(sum(weight**2 for weight in doc_weights.values()))
    if norm > 0:
        doc_weights = {term: weight / norm for term, weight in doc_weights.items()}

    return doc_weights


def compute_cosine_similarity(
    query_weights: dict[str, float], doc_weights: dict[str, float]
) -> float:
    dot_product: float = sum(
        query_weights.get(term, 0) * doc_weights.get(term, 0)
        for term in set(query_weights.keys()) | set(doc_weights.keys())
    )
    query_norm: float = sqrt(sum(weight**2 for weight in query_weights.values()))
    doc_norm: float = sqrt(sum(weight**2 for weight in doc_weights.values()))
    if query_norm == 0 or doc_norm == 0:
        return 0
    return dot_product / (query_norm * doc_norm)


def rank_documents(query: str) -> list[int]:
    query_terms: list[str] = query.lower().split()
    query_weights: dict[str, float] = compute_query_weights(query_terms)

    doc_scores: dict[int, float] = {}
    for doc_id in range(1, NUM_DOC + 1):
        doc_weights: dict[str, float] = compute_doc_weights(doc_id, query_terms)
        doc_scores[doc_id] = compute_cosine_similarity(query_weights, doc_weights)

    return sorted(doc_scores, key=doc_scores.get, reverse=True)
