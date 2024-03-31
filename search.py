#!/usr/bin/python3
import getopt
import heapq
import math
import re
import sys
import time
from collections import Counter, defaultdict
from operator import index

import nltk

from indexer import Indexer
from preprocessor import Preprocessor


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
    start_time = time.time()
    with Indexer(dict_file, postings_file) as indexer:
        with open(queries_file, "r") as in_file, open(results_file, "w") as out_file:
            is_first_line: bool = True
            N = indexer.num_docs

            for query in in_file:
                query = query.rstrip("\n")
                terms_freq = Counter(Preprocessor.tokenize(query))
                query_norm = math.sqrt(sum(tf**2 for tf in terms_freq.values()))

                scores: dict[int, float] = defaultdict(lambda: 0.0)
                for term, tf in terms_freq.items():
                    df, postings_list = indexer.get_term_data(term)
                    if tf == 0 or df == 0:
                        continue

                    query_weight = (1 + math.log10(tf)) * math.log10(N / df)

                    for doc_id, tf in postings_list:
                        doc_weight = 1 + math.log10(tf)
                        scores[doc_id] += doc_weight * query_weight

                for doc_id in scores.keys():
                    scores[doc_id] /= indexer.doc_norm_lengths[doc_id] * query_norm

                heap_items = [(-score, doc_id) for doc_id, score in scores.items()]
                top_items = heapq.nsmallest(10, heap_items)
                relevant_docs = [doc_id for _, doc_id in top_items]

                padding = "" if is_first_line else "\n"
                out_file.write(padding + " ".join(map(str, relevant_docs)))
                is_first_line = False
    end_time = time.time()
    print(f"Execution time: {end_time - start_time}s")


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
