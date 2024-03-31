from typing import Iterator

import nltk


class Preprocessor:
    """Handles the preprocessing of documents and tokens."""

    stemmer = nltk.PorterStemmer()

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Tokenize a single sentence.

        Preprocessing applied in order of execution:
        - Case-folding to lowercase.
        - Word tokenization using `nltk.word_tokenize`.
        - Stemming using `nltk.PorterStemmer`.
        """
        return [
            Preprocessor.stemmer.stem(token).lower()
            for sentence in nltk.sent_tokenize(text)
            for token in nltk.word_tokenize(sentence)
        ]

    @staticmethod
    def to_token_stream(filepath: str) -> Iterator[str]:
        """Read the ENTIRE file at `filepath`, apply the below preprocessing
        before yielding the tokens one-by-one.

        Preprocessing applied in order of execution:
        - Case-folding to lowercase.
        - Sentence tokenization using `nltk.sent_tokenize`.
        - Word tokenization using `nltk.word_tokenize`.
        - Stemming using `nltk.PorterStemmer`.

        Args:
            filepath (str): Path to the file to tokenize.

        Yields:
            Iterator[str]: Tokens from the file.
        """
        with open(filepath, "r") as file:
            doc_text = file.read()

            for sentence in nltk.sent_tokenize(doc_text):
                for token in nltk.word_tokenize(sentence):
                    yield Preprocessor.stemmer.stem(token).lower()
