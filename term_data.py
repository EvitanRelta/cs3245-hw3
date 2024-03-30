from dataclasses import dataclass


@dataclass
class TermData:
    """Data related to a term."""

    doc_freq: int
    """Document frequency of term."""

    term_freq_dict: dict[int, int]
    """Dict in the form: { docID: term_freq }."""
