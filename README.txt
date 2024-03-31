This is the README file for A0000000X's submission
Email(s):
- e0727143@u.nus.edu
- e0725753@u.nus.edu

== Python Version ==

We're using Python Version 3.10.12 for this assignment.

== General Notes about this assignment ==

The program was implemented under the assumption that the dictionary can be held in memory. As such, no scalable index construction technique was used when indexing.

# Flow for Indexing 
1. Initialize an in-memory index.
1. Iterate through each document in the training dir one-by-one.
2. For each document, preprocessing is done by the steps in order:
    1. Read the entire document into memory.
    2. Case-fold to lowercase.
    3. Tokenize into sentences via `nltk.sent_tokenize`.
    4. Tokenize each sentence via `nltk.word_tokenize`.
    5. Stem each token via `nltk.PorterStemmer`.
3. For each document, we use a Counter to:
    1. Append (doc_id, term_freq) to the term in main index
    2. Calculate normalized length for document
4. Once all documents has been accounted, we iterate through the index,
   and create `dictionary.txt` and `postings.txt` in the format:
    1. `dictionary.txt` contains:
       ```
       1st line: 1st term, document-frequency, byte-offset, size of posting list in `postings.txt`
       2nd line: 2nd term, document-frequency, byte-offset, size of posting list in `postings.txt`
       ...
       n+1 line: document id, normalized document length
       ```
    2. `postings.txt` contains:
       ```
       1st line: Posting list for 1st term in `dictionary.txt` as whitespace separated (doc_id, term_freq)
       2nd line: Posting list for 2nd term in `dictionary.txt` as whitespace separated (doc_id, term_freq)
       ...
       ```

--------- DOCUMENT INDEXING HAS COMPLETED HERE ---------

# Flow for searching
1. The terms, document-frequencies, byte-offsets and sizes are loaded into memory and rebuilt via `indexer.py`.
2. For each query, we preprocess (exactly as above) by:
    1. Case-fold to lowercase.
    2. Tokenize each sentence via `nltk.word_tokenize`.
    3. Stem each token via `nltk.PorterStemmer`.
3. For each query term, we use the rebuilt index to:
    1. Retrieve the document frequency. If 0, we skip the query term.
    2. Calculate Log TF-IDF for query term
    3. Calculate Log TF of all documents
    4. Accumulate similarity scores
4. Peform cosine normalization on the scores of each doc_id
5. Heapify scores and retrieve top 10, tie-break using doc_id 


# Design decisions

1. Reading each document whole (instead of line-by-line).
   Because the sentences in the "reuters" documents are often split across
   multiple lines. Thus, reading line-by-line might break up sentences and
   `nltk.sent_tokenize` won't work properly.


== Files included with this submission ==

# Misc. Files:
README.txt        - Overview.
dictionary.txt    - Contains the terms, document frequencies, byte-offsets
                    and sizes for the corresponding posting list in 'postings.txt'.
                    Contains document id and normalized length for each of the
                    documents.
postings.txt      - Contains the posting lists for all terms, formatted as
                    (doc_id, term_freq)

# Files used in both indexing/searching:
preprocessor.py   - Handles preprocessing tasks (eg. stemming and tokenization of training docs and queries.)

# Files used during indexing:
index.py          - Main entry for building the dictionary and postings llist

# Files used during searching:
search.py         - Main entry for search query
indexer.py        - Handles retrieving the postings lists by reading `dictionary.txt` and `postings.txt`.


== Statement of individual work ==

[x] We, A0235143N-A0233753E, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

We suggest that we should be graded as follows:

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
