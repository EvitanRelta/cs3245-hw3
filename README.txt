This is the README file for A0235143N-A0233753E's submission
Email(s):
- e0727143@u.nus.edu
- e0725753@u.nus.edu

== Python Version ==

We're using Python Version 3.10.12 for this assignment.

== General Notes about this assignment ==



The program was implemented under the assumption that the dictionary can be held in memory.
As such, no scalable index construction technique was used when indexing.

# Flow for Indexing 

1. Initialize in-memory dicts for the normalized document length and inverted-index.
2. Iterate through each document in the training dir one-by-one.
3. For each document, preprocessing is done by the steps in order:
    1. Read the entire document into memory.
    2. Tokenize into sentences via `nltk.sent_tokenize`.
    3. Tokenize each sentence via `nltk.word_tokenize`.
    4. Stem each token via `nltk.PorterStemmer`.
    5. Case-fold to lowercase.
4. For each document, we compute:
    1. compute its normalized length:
       sqrt(sum( (1 + log(tf)) ^ 2 for each term ))
    2. append its (doc_id, term_freq) to the term's postings-list
5. Once all documents has been accounted, we iterate through the index,
   and create `dictionary.txt` and `postings.txt` in the format:

    1. `dictionary.txt` contains:
       ```
       TERM DF OFFSET SIZE   # eg. bahia 4 0 37
       TERM DF OFFSET SIZE
       ...

       DOC_ID NORMALIZED_DOC_LENGTH   # eg. 1 18.743376382392842
       DOC_ID NORMALIZED_DOC_LENGTH
       ...
       ```

       where OFFSET and SIZE are used to seek/read the postings-list associated
       with the term, and the normalized doc lengths are seperated from the
       inverted-index by an empty line.

    2. `postings.txt` contains:
       ```
       (DOC_ID,TF) (DOC_ID,TF) ...   # eg. (1,4) (11459,2) (11911,3) (13462,1)
       (DOC_ID,TF) (DOC_ID,TF) ...
       ...
       ```



# Flow for Searching

1. The terms, document-frequencies, byte-offsets, sizes and normalized document
   lengths are loaded into memory via the `Indexer` class in `indexer.py`.
2. For each query, we preprocess (same as for documents) by:
    1. Tokenize into sentences via `nltk.sent_tokenize`.
    2. Tokenize each sentence via `nltk.word_tokenize`.
    3. Stem each token via `nltk.PorterStemmer`.
    4. Case-fold to lowercase.
3. To retrieve a term's posting list:
    1. Get the term's "offset" and "size" from the in-memory dict.
    2. Seek to the "offset" byte in `postings.txt` file.
    3. Read "size" number of bytes.
    6. Parse the read text, into a `LinkedList` instance (defined in `linked_list.py`).
4. For each term in the query:
    1. Retrieve the document frequency (DF) and postings-list.
       If the term doesn't exist in any document (ie. DF=0), we skip that term.
    2. Calculate query weight (ie. log TF-IDF):
       (1 + log(tf)) * log(N / df)
    3. Calculate document weights (ie. log TF) for all documents in the term's postings-list:
       (1 + log(tf))
    4. Multiply the query and document weights for that term.
    5. Accumulate similarity scores.
5. Peform cosine normalization on the scores of each doc_id.
6. Sort and retrieve the top 10 highest-scoring doc-ID, tie-breaking with doc-ID.



# Design decisions

1. Reading each document whole (instead of line-by-line).
   Because the sentences in the "reuters" documents are often split across
   multiple lines. Thus, reading line-by-line might break up sentences and
   `nltk.sent_tokenize` won't work properly.

2. Case-folding is done as the last preprocessing step (after stemming) as per
   Prof's advice on Piazza: https://piazza.com/class/lqnh8c1ml6q50b/post/147

2. Postings-lists during search are represented as LinkedList (without
   skip-pointers) instead of Python lists as per Piazza post 151:
   https://piazza.com/class/lqnh8c1ml6q50b/post/151.

   Although this significant slows performance
   (58s with Python lists, 101s with linked-lists).

3. Due to floating-point inaccuracies, documents with the same scores can end
   up having slightly different float values during computation
   (eg. 0.8 vs 0.80000000001).

   Thus, we use `math.isclose` to treat very similar scores as the same (and
   hence be ranked by their doc-IDs instead). This is implemented in the
   `compare_tuples` function in `search.py`.

4. Heap is used to obtained the top 10 relevant doc-IDs, as it's faster than
   sorting the whole list.


== Files included with this submission ==

# Misc. Files:
README.txt        - Overview.
dictionary.txt    - Contains:
                    1. the terms, document frequencies, byte-offsets and sizes
                       for the corresponding posting list in 'postings.txt'.
                    2. and the normalized length for each of the documents.
postings.txt      - Contains the posting lists for all terms, formatted as
                    (doc_id, term_freq).

# Files used in both indexing/searching:
preprocessor.py   - Handles preprocessing tasks (eg. stemming and tokenization of training docs and queries).
linked_list.py    - Linked-list implementation.

# Files used during indexing:
index.py          - Main entry for building the dictionary and postings-list files.

# Files used during searching:
search.py         - Main entry for search query
indexer.py        - Handles retrieving the doc-lengths, doc-frequencies, postings
                    lists by reading `dictionary.txt` and `postings.txt`.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

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
