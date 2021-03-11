import sys
import nltk
from nltk import pos_tag
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *  
import shelve
import time
import collections
from operator import itemgetter
lemclass = WordNetLemmatizer()
stemmer = SnowballStemmer('english')
import operator
import time

class TheFinder():
    """ Search engine using data from compressed files created in ldamodel-program.
        costumized input from terminal is used as argument in second method.

    Attributes:
        self.lemnstemwords:     list of all words from input, lemmatized and stemmed
        self.id_input:          list of index number of inputwords
        self.besttopicstot:     list of tuples with topic as first element and weight of topic. Tuples 
                                sorted by lightest weight first and heaviest last  
        self.besttopicstot_only:    list of topics sorted after relevance, most relevant topic being first
        self.priowords:         list of words relevant articles should contain, being input words and words 
                                 from the most relevant topic. Sorted after most relevant word(index) in falling order 
        self.artsforoutputsorted:   articles (indexnumbers) sorted after relevance, most relevant article being first 
                                    in order.   
        self.artslist_length:   sum of total hits of search
        """

    def __init__(self):
        """ Create a TheFinder object and empty attributes.
            """
        self.lemnstemwords = []
        self.id_input = []

    def lemsteminput(self,inputsplit):
        """ Lemmatize and stem inputwords and find indexnumber of these. If indexnumber/s cannot be found,
            a message containing this information is printed.
    
        Argument:
            inputsplit:     list of words from input(), lemmatized and stemmed. 
            """
        for w in in_words:
            lemochstemmad = stemmer.stem(lemclass.lemmatize(w, convert_pos(w)))
            self.lemnstemwords.append(lemochstemmad)
        with shelve.open('shelve_tokenid17') as wordconv: 
            for word in self.lemnstemwords:
                if word in wordconv:
                    in_index = wordconv[word]           #Finds word-id of input words
                    self.id_input.append(in_index)
                else:
                    print (word,'does not exist in the search engine')  
                                
    def best_topic(self):    
        """ Sort topics by best suited based on inputwords 
            """
        toplist = []        #long list of lists of place in topics
        toplisttop = {}     # collected "weights" for topics
        with shelve.open('shelve_topicprio17') as besttop:
            for word in self.id_input:
                word = str(word)
                topics = list(besttop[word].items())
                toplist.append(topics)  
        for word in toplist:
            for top in word:
                 if top[0] not in toplisttop:
                    toplisttop[top[0]] = top[1] 
                 else:
                    toplisttop[top[0]] += top[1]
        self.besttopicstot = sorted(toplisttop.items(), key=operator.itemgetter(1))        
        self.besttopicstot_only = []
        for pair in self.besttopicstot:
            self.besttopicstot_only.append(pair[0])

    def find_prio_words(self):
        """ Find and sort words that are to be searched for in article based on total frequency and most suitable topic.
            """
        self.priowords = []
        tuplefreq = []      #list with word-id and weight
        besttopic = self.besttopicstot_only[0]
        with shelve.open('shelve_tptoplist17') as toplist:
            besttopicwords = toplist[besttopic]
            for word in besttopicwords:
                if word in self.id_input:
                    besttopicwords.remove(word)
        with shelve.open('shelve_bowaktig17') as findfreq:          # weights of words are based on how common the words are in the data 
            for word in self.id_input:
                totalfreq = sum(findfreq[str(word)].values())
                weight = 1 / totalfreq
                tuplefreq.append((word,weight)) 
            for word in besttopicwords:      
                totalfreq = sum(findfreq[str(word)].values())
                weight = (1 / totalfreq)/2                          # topic words weights are halfened to make up for 
                tuplefreq.append((word,weight))                     # ... not being as relevant as seach words (input words)
            tuplefreq.sort(key=lambda tup: tup[1], reverse=True)
            
        self.priowords = tuplefreq
        with shelve.open('shelve_idtoken17') as translate:
            for tup in self.priowords:
                id = str(tup[0])
        
    def find_best_articles(self):
        """ Detect and sort best suited articles for output based on self.priowords.
            """
        artsforoutput = {}    
        with shelve.open('shelve_bowaktig17') as bowakt:
            for ord in self.priowords:
                ordid = str(ord[0])  
                ordvikt = ord[1] 
                artsnfreq_ofword = bowakt[ordid]
                for art in artsnfreq_ofword:
                    if art not in artsforoutput:
                        artsforoutput[art] = ordvikt
                    else:
                        artsforoutput[art] += ordvikt
        self.artsforoutputsorted = collections.OrderedDict(sorted(artsforoutput.items(), key = itemgetter(1), reverse = True))                        


    def printarticles20(self):
        """ Print unprocessed article along with headline based on self.artsforoutputsorted attrubute.
            Also, save all printed dokuments and headlines to compressed dictionary-file (shelve-file) 
    
        Prints:
                Unprocessed headlines and articles
            """
        save = {}
        artslist = self.artsforoutputsorted.keys() 
        self.artslist_length = len(artslist)
        with shelve.open('shelve_headlines17') as headl:
            with shelve.open('shelve_oprocessat17') as oproc:
                i = 1
                for art in artslist:
                    article_id = str(art)
                    headline = headl[article_id]
                    whole_article = oproc[article_id]
                    headl_and_art = str('Hit ') + str(i) + '   ' + headline + '       ' + whole_article
                    save[str(i)] = headl_and_art
                    if i < 11:
                        print ('\033[31m' + str('Hit ') + str(i) +'\033[0m')
                        print (headline)
                        print (whole_article + '\n')
                        i += 1
                    else:
                        i += 1
 
        with shelve.open('shelve_results') as resu:   
            key = (' ').join(in_words)
            resu[key] = save            # if same search has been done before, it is replaced by the new search.
          
        print ('\033[1m' +'Search words: ' + key + '\033[0m') 
                    
def convert_pos(word):
    """ Function used for lemmatization of input words.

    Arg:
        a string that is a word
    
        Returns:
            suitable POS-tag for lemmatization of argument
        """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,"N": wordnet.NOUN, "V": wordnet.VERB,"R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN) 
 
            
if __name__== "__main__":
    learnword = 'dog'
    print ('\033[1m' + "What are you looking for?" + '\033[0m')
    learnconvert_pos = stemmer.stem(lemclass.lemmatize(learnword, convert_pos(learnword)))  # initialization of convert_pos takes
    searchobject = TheFinder()                                              # ...3 seconds, so therefore it is initialized as soon as
    in_words = input().split()                                          # ... the program is started.
    searchobject.lemsteminput(in_words)
    searchobject.best_topic()
    searchobject.find_prio_words()
    searchobject.find_best_articles()
    searchobject.printarticles20()    
    print ('\033[1m' +"For certain hits or all", searchobject.artslist_length, ", remember Search words and see Find_hits.py" + '\033[0m')
    
