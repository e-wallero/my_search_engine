## Table of contents
* [Introduction](#introduction)
* [Converter](#converter)
* [Ldamodel and compressor](#ldamodel_and_compressor)
* [Search engine](#search_engine)
* [Saved searches](#saved_searches)


Welcome to the README-file for "Search engine" - project in tillämpad
programmering för lingvister

By Emma Wallerö 2020-01-17

## Introduction

This search engine is based on data from the english gigaword corpora.
The specific data used are news articles from "Central News Agency of Taiwan,
English Service" from year 1997 to 2010. These are 144 gzip-files containing
around 300.000 words each. Similar data from six other english news sources
can be found in the corpora, and can be used for the converter class, LDA model
and compressor class, and search engine class too.

Note: To run the search engine a lda-model must be trained. No pre-trained
model is available in this repository due to usage of licensed data.
English Gigaword Fifth Edition source can be obtained here:
https://catalog.ldc.upenn.edu/LDC2011T07 


## Converter
(converter.py)

The converter class converts words, headlines and articles to index numbers in
three different attributes in forms of dictionaries. Information of word
frequencies in total data and "bag of words"-list with information about word
frequencies in specific articles are also saved as class attributes: These
attributes are needed for next class, the LDA model and compressor class.

## Ldamodel and compressor
(ldamodel_and_compressor.py)

The LDA model-class methods creates a topic model with four topics based on
data from the converter class. The final method of this class compresses and
saves data necessary for the search engine, to shelve-files. These data contain
information about word, headline and article ids, word frequency information,
and topic model information. Run-time of this program with the CNA-data is
circa 1,5 days.


## Search engine
(Emmas_search_engine.py)

When the user runs the search engine file, the user is asked to type in search
words in the terminal. The class object uses data from the shelve files created
in the LDA model class. Input word/words are lemmatized and stemmed. Then, best
suitable topic is retrieved, and a list of input words and topic words is
compiled in order of "heaviest" weight in falling order. Based on this list of
words, articles are retrieved ordered after relevance. The top ten most
relevant articles are printed out in the terminal. To see all hits or only
certain hits, the results can be found easily by starting the Find hits-program.


## Saved searches
(Find_hits.py)


This is a simple program for viewing the hits of your searches. Instructions
for how to use it are printed out as the program is started. The input should
be formed in this manner: a recent search of yours : start of range, end of
range. Example: dogs and cats in China : 1, 20
