#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import math
import os
from preprocessor import Preprocessor
from collections import Counter

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below


    filenames = [int(x) for x in os.listdir(in_dir)]
    normalized_lengths = {}
    index = {}

    for filename in sorted(filenames):
        filepath = in_dir + str(filename)

        # Each document has its own counter to keep track of the internal counts
        counter = Counter()

        # Iterate through document and maintain count
        for token in Preprocessor.to_token_stream(filepath):
            counter.update([token])

        # Accumulate and compute normalized length
        normalized_length = 0
        for term_frequency in counter.values():
            normalized_length += term_frequency ** 2

        normalized_lengths[filename] = math.sqrt(normalized_length)
        
        # Update the index with local counts
        for term, term_frequency in counter.items():
            postings_list = index.get(term, [])
            postings_list.append((filename, term_frequency))
            index[term] = postings_list

    # Write out the normalized lengths to doc_length.txt
    with open('./doc_lengths.txt', 'w') as olen:
        for docid, length in normalized_lengths.items():
            olen.write(f'{docid} {length}\n')

    with open(out_dict, 'w') as odict, open(out_postings, 'w') as opost:
        start_offset = 0

        # Write out the term and document frequency
        for term, postings_list in index.items():
            # whitespace separated (doci, term_freq)
            opost.write(f'{" ".join([f"({id_freq[0]},{id_freq[1]})" for id_freq in postings_list])}\n')
            end_offset = opost.tell()
            size = end_offset - start_offset

            # whitespace separated - term doc_freq start size
            odict.write(f'{term} {len(postings_list)} {start_offset} {size}\n')
            start_offset = end_offset


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
