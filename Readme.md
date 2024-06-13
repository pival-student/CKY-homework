### Description
Homework 4 sample solution:

A base Python 3 implementation of a CKY parser with some helper functions,
following the [wikipedia pseudocode](https://en.wikipedia.org/wiki/CYK_algorithm)
### Requirements
Python 3 (Python 3.10+ recommended)
### Usage
Via terminal:
*python parser.py [-h] grammar sentences output_dir*

Parses a file of sentences with a provided context-free grammar

positional arguments:

* grammar:     A context-free grammar file
* sentences:   A file containing one sentence per line
* output_dir:  A directory to write the parse result file to

options:
  -h, --help  show this help message and exit