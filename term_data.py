from dataclasses import dataclass


@dataclass
class TermData:
    doc_freq: int
    """Document frequency of term."""

    term_freq_dict: dict[int, int]
    """Dict in the form: { docID: term_freq }."""
