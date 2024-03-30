#!/usr/bin/python3
import getopt
from operator import index
import re
import sys

import nltk

from indexer import Indexer
from utils import cosine_similarity, get_tf_idf
from preprocessor import Preprocessor
from collections import Counter


def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"
    )


def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print("running search on the queries...")
    with Indexer(dict_file, postings_file) as indexer:
        with open(queries_file, "r") as in_file, open(results_file, "w") as out_file:
            for query in in_file:
                query = query.rstrip("\n")

                terms = Preprocessor.tokenize(query)
                terms_freq = Counter(terms)

                score: float = 0
                for term,term_freq in terms_freq.items():
                    term_data = indexer.get_term_data(term)
                    tf_idf = get_tf_idf(term_freq, term_data.doc_freq, indexer.num_docs)

                

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


                indexer.get_term_data()

                result_postings = query_parser.parse_query(query)

                newline = "" if is_first_line else "\n"
                out_file.write(newline + " ".join(map(str, result_postings)))
                is_first_line = False


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:p:q:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == "-d":
        dictionary_file = a
    elif o == "-p":
        postings_file = a
    elif o == "-q":
        file_of_queries = a
    elif o == "-o":
        file_of_output = a
    else:
        assert False, "unhandled option"

if (
    dictionary_file == None
    or postings_file == None
    or file_of_queries == None
    or file_of_output == None
):
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
