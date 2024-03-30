from term_data import TermData


class Indexer:
    """Handles getting the inverted-index from the dictionary and postings files."""

    def __init__(self, dict_file_path: str, postings_file_path: str) -> None:
        """
        Args:
            dict_file_path (str): Path to file containing the offsets and sizes for each term, and \
                all the doc lengths.
            postings_file_path (str): Path to file containing all the postings list.
            doc_length_path (str): Path to file containing all doc lengths.
        """
        self.postings_file_io = open(postings_file_path, "rb")
        self.term_metadata, self.doc_lengths = self._load_data_from_dict_file(dict_file_path)

    def __enter__(self) -> "Indexer":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        """Close any file IOs."""
        self.postings_file_io.close()

    @staticmethod
    def _load_data_from_dict_file(
        dict_file_path: str,
    ) -> tuple[dict[str, tuple[int, int, int]], dict[int, float]]:
        """Loads the data from the dictionary file into memory.

        Returns:
            tuple[dict[str, tuple[int, int, int]], dict[int, float]]: \
                `(term_metadata, doc_lengths)`.
        """
        term_metadata: dict[str, tuple[int, int, int]] = {}
        doc_lengths: dict[int, float] = {}

        with open(dict_file_path, "r") as f:
            for line in f:
                if line == "\n":
                    break
                term, doc_freq, offset, size = line.rstrip("\n").split()
                term_metadata[term] = int(doc_freq), int(offset), int(size)

            for line in f:
                if line == "\n":
                    break
                docid, length = line.rstrip("\n").split()
                doc_lengths[int(docid)] = float(length)

        return term_metadata, doc_lengths

    def get_term_data(self, term: str) -> TermData:
        """Gets the postings list for `term`."""
        doc_freq, offset, size = self.term_metadata[term]
        self.postings_file_io.seek(offset)
        raw_postings_str = self.postings_file_io.read(size).decode().rstrip("\n")

        term_freq_dict: dict[int, int] = {}
        for s in raw_postings_str:
            docid, term_freq = s.rstrip(")").lstrip("(").split(",")
            term_freq_dict[int(docid)] = int(term_freq)
        return TermData(doc_freq, term_freq_dict)
