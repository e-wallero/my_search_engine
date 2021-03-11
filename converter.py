from operator import itemgetter    
import nltk
from nltk import pos_tag
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import * 
import gensim       
from gensim import corpora
import gzip
from collections import Counter
from gensim.parsing.preprocessing import STOPWORDS
import glob
import re  
import string

class Converter:
    """ Converter converting words, headlines and articles to indexnumbers.
        Necessary information for topic model and search engine is saved as
        attributes: total word frequencies, word frequencies per article, 
        and unprocessed articles. 

    Attributes:
        self.word_index:    dictionary with indexnumber(int) as key and word(str) as value 
        self.dokuname_index:      dictionary with indexnumber(int) as key and headline(str) as value 
        self.lemmatize:     lemmatizer from nltk module
        self.wordfreqdict:  corpora-dictionary object from gensim module with word(str) as key and
                            total frequency as value
        self.docs:          dictionary with indexnumber(int) as key and unprocessed article as value
        self.all_lemnstem:  A list of lists for each article. In articles list there are lemmatized and
                            stemmed words in order of occurence in unproccesed article. 
        self.bow:           A "bag of words". List of lists for each article. inside each articles list
                            are tuples with word-index as first element, and frequency in document
                            as second element 
        """
    
    def __init__(self):        
        """ Create a Converter object and empty attributes
            """
        self.word_index = {}       
        self.dokuname_index = {}
        self.lemmatize = WordNetLemmatizer()      
        self.wordfreqdict = corpora.Dictionary()
        self.docs = {}
        
    def lemstem_convert(self,dirname):
        """ Save necessary data from argument to class object-attributes
              
        Arg:
            dirname:    name of directory containing news article data    
            """
        self.all_lemnstem = []          
        lemclass = WordNetLemmatizer()
        stemmer = SnowballStemmer('english')
        headl = None        # variable used for detecting headlines       
        print (dirname)
        print (glob.glob(dirname + '/*[0-9].gz'))
        for dokument in glob.glob(dirname +'/*[0-9].gz'):
            print (dokument)
            i = 0
            with gzip.open(dokument, 'rt') as file:
                sentence = []   #  will consist of one articles lemmatized and stemmed words in order.
                orordart = []  
                for line in file:
                    i += 1
                    if not line.strip():
                        continue     
                    else:
                        if '<HEADLINE>' in line:
                            headl = 'yes'       
                            continue        
                        elif headl == 'yes':    
                            if self.dokuname_index == {}:   # This if-statement only happens when the first headline is processed
                                newindex = len(self.dokuname_index)
                                articlename = line[:-1]  
                                self.dokuname_index.setdefault(newindex,articlename) 
                                headl = None                    
                            else:                                   # data is saved to attributes
                                self.all_lemnstem.append(sentence)   
                                helart = ' '.join(orordart)
                                self.docs.setdefault(newindex,helart)
                                sentence = []      
                                orordart = []
                                newindex = len(self.dokuname_index)
                                articlename = line[:-1]
                                self.dokuname_index.setdefault(newindex,articlename)
                                headl = None
                        elif '<' and '>' in line:       # Lines with formation information are not saved 
                            headl = None
                            continue
                        else:                  # This is where lines containing article-data (not headlines) are processed
                            headl = None       # ... before they are saved to attributes
                            tokline = line.split()
                            for tok in tokline:
                                orordart.append(tok)
                                word = tok.lower().strip(string.punctuation)
                                if word in gensim.parsing.preprocessing.STOPWORDS or len(word) < 3: 
                                    continue     
                                else:
                                    ready = stemmer.stem(lemclass.lemmatize(word, convert_pos(word)))
                                    sentence.append(ready)
        self.bow = [self.wordfreqdict.doc2bow(doc, allow_update=True) for doc in self.all_lemnstem]   # self.wordfreqdict is
                        # ... updated and self.bow created with help from information from self.all_lemnstem and gensim corpora
  
def convert_pos(word):
    """ Function used in lemstem_convert-method for lemmatization of word.

    Arg:
        a string that is a word

    Returns:
        suitable POS-tag for lemmatization of argument
        """
    tag = nltk.pos_tag([word])[0][1][0].upper()     # POS-tag is collected with nltk-module and pos_tag method. 
    tag_dict = {'J': wordnet.ADJ,'N': wordnet.NOUN, 'V': wordnet.VERB,'R': wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)          # If "tag" does not respond to any key in tag_dict, a default noun POS-tag is returned
   
if __name__== "__main__":
    classobj = Converter()
    classobj.lemstem_convert('/home/lin205_emwa8882/ht19/projekt/testdir/test2dir')


# Source I used on using gensim module for this type of purpose:
# https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24 
  
# Source I used on wordnet POS-tagging:
# https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
