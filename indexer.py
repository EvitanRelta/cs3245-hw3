class Indexer:
    """Handles getting the inverted-index from the dictionary and postings files."""

    def __init__(self, dict_file_path: str, postings_file_path: str, doc_length_path: str) -> None:
        """
        Args:
            dict_file_path (str): Path to file containing the offsets and sizes for each term.
            postings_file_path (str): Path to file containing all the postings list.
            doc_length_path (str): Path to file containing all doc lengths.
        """
        self.dict_file = open(dict_file_path, "r")
        self.postings_file = open(postings_file_path, "rb")
        self.doc_length_file = open(doc_length_path, "r")

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        """Close any file IOs."""
        self.dict_file.close()
        self.postings_file.close()
        self.doc_length_file.close()

    def rebuild_index(self) -> dict[str, list[list[str]]]:
        rebuilt_index = {}
        for line in self.dict_file:
            if line == "\n":
                continue
            term, doc_freq, offset, size = line.rstrip("\n").split()
            rebuilt_index[term] = self._get_postings(int(offset), int(size))

        return rebuilt_index

    def _get_postings(self, offset: int, size: int) -> list[list[str]]:
        self.postings_file.seek(offset)
        postings_str = self.postings_file.read(size).decode().rstrip("\n").split()
        postings_list = list(map(lambda x: x.rstrip(")").lstrip("(").split(","), postings_str))
        return postings_list

    def index_doc_length(self) -> dict[int, float]:
        doc_length_index = {}
        for line in self.doc_length_file:
            docid, doc_length = line.rstrip("\n").split()
            doc_length_index[int(docid)] = float(doc_length)

        return doc_length_index
