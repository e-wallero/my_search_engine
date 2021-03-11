from converter import *
import gensim
from gensim import corpora
from gensim.utils import simple_preprocess
import numpy as np
from gensim import models
from gensim.models import TfidfModel
from gensim.models.ldamulticore import LdaMulticore
from pprint import pprint
import shelve
from operator import itemgetter
import time

class ldamodel(): 
    """ Ldamodel of data from converter-class. Compression of necessary data for search enginge is made.

    Attributes:
        self.convclass:     converter-object used for ldamodel and compression
        self.corp_tfidf:    tfi-idf values for words in data    
        self.tpalla:        topics with all words and weights in falling order
        """
    def __init__(self, directory):
        """ Create an ldamodel object with empty attributes.   

        Arg:
            directory: directory of files of news article data
            """
        convclass = Converter() 
        convclass.lemstem_convert(directory) 
        self.convclass = convclass 
             
    def tf_idf(self):
        """ Create tf-idf weights for topic model and save to attribute self.corp_tfidf. """
        tfidf = models.TfidfModel(self.convclass.bow)
        self.corp_tfidf = tfidf[self.convclass.bow]
    
    def make_tmTFIDF(self):
        """ Make LDA-type topic model with 4 topics"""
        self.lda_modeltfidf = gensim.models.LdaMulticore(self.corp_tfidf, num_topics=4, passes=2, workers=4)
        self.tpalla = self.lda_modeltfidf.show_topics(num_topics=4,num_words=10000000000, log=False, formatted=True) # Topicmodel with 
   #... all words in from data set. Hypothetically, if data contained more than 10 000 million words were used, you would have to adjust num_words to a larger amount 

    def save_shelve(self):
        """ Create compressed files (shelves) with all necessary data for search engine.    
    
        Form of shelves:
            shelve_bowaktig:     Key: word-id(string)   Value: dictionary with key: article-id, value: frequency of word  
            shelve_tokenid:      Key: word-token(string)     Value: word-id
            shelve_idtoken:      inverted version of shelve_tokenid
            shelve_tpalla:       Key: topic     Value: dictionary with key: word-id, value: place in topic  # This attribute is unecessary in seach engine
            shelve_tptoplist:    Key: topic     Value: List of 10 word-ids with heaviest weight in topic
            shelve_topicprio:    Key: word-id   Value: dictionary with key: topic, value: place of word-id in topic
            shelve_oprocessat:   Key: article-id    Value: unprocessed article
            shelve_headlines:    Key: headline-id   Value: headline 
            """
        with shelve.open('shelve_bowaktig207') as she:
            art_i = 0
            dictofwords = {}  
            for art in self.convclass.bow:
                for tup in art:
                    strword = str(tup[0])
                    freq = tup[1]
                    if strword not in dictofwords:
                        dictofwords[strword] = {art_i : freq}
                    else:
                        dictofwords[strword][art_i] = freq
                art_i += 1
            for key, value in dictofwords.items():
                she[key] = value    

        with shelve.open('shelve_tokenid207') as she:
            with shelve.open('shelve_idtoken207') as shereverse:
                for key, value in self.convclass.wordfreqdict.items():
                    she[str(value)] = key
                    shereverse[str(key)] = value                
                     
        with shelve.open('shelve_tpalla207') as she:            # This shelve-file is not used in final version of seach engine,
            with shelve.open('shelve_tptoplist207') as shetop:  # ... but it has not been removed since it is part of how the 
                shlist = []                                     # ...class looked when data for search engine was collected last.
                for topic in self.tpalla:        
                    baratop = str(topic[0])
                    entopic = {}
                    shetoplist = []
                    listofwords = topic[1].split('+')
                    i = 0
                    for ordovikt in listofwords:
                        wordid = int(ordovikt.split('"')[1])
                        entopic[wordid] = i
                        if i < 9:
                            shetoplist.append(wordid)
                            i += 1
                        else:
                            i += 1
                    she[baratop] = entopic        
                    shetop[baratop] = shetoplist

        topics_num = ['0','1','2','3']  # If number of topics is changed, this list must be altered too. it should
        with shelve.open('shelve_topicprio207') as sheprio:                 # ... correspond to number of topics.
             with shelve.open('shelve_tpalla207') as shetpalla:
                dictofwords = {}
                for top in topics_num:   
                    for word in shetpalla[top]:
                        place = shetpalla[top][word]
                        if word not in dictofwords:
                            dictofwords[word] = {top:place}
                        else:
                            dictofwords[word][top] = place
             for word in dictofwords:
                sheprio[str(word)] = dictofwords[word] 
       
        with shelve.open('shelve_oprocessat207') as she:
            for art in self.convclass.docs:
                she[str(art)] = self.convclass.docs[art]
        
        with shelve.open('shelve_headlines207') as headl:
            i = 0    
            for art in self.convclass.dokuname_index:
                headl[str(art)] = self.convclass.dokuname_index[art]


if __name__== "__main__":
    lda_classobject = ldamodel('/home/corpora/gigaword_eng_5/gigaword_eng_5_d2/data/cna_eng') 
    lda_classobject.tf_idf()
    lda_classobject.make_tmTFIDF()
    lda_classobject.save_shelve()
