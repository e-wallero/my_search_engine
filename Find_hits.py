import sys
import shelve

def findthehits(searchandrange):
    """ Find arbitrary range of hits from old search from Emmas_search_engine
    
    Arguments:
        searchandrange:     search word searched for in Emmas_search_engine (in order) and range of hits (int,int)
    
    Prints:
        Hits from search in chosen range        
    """

    keyandrange = searchandrange.split(':')
    key = keyandrange[0].strip()
    range = keyandrange[1].strip().split(',')
    with shelve.open('shelve_results') as resu:
        if len(range) == 1:
            hit = keyandrange[1]
            print ('Hit ' + hit +': ' + resu[key][hit])
        else: 
            toprint = range
            i_start = int(toprint[0])
            i_stop = int(toprint[1])
            i = i_start
            lengthlist = 'o' * ((i_stop - i_start) +1)         # list with same lengh as chosen range for next for-loop
            for x in lengthlist:
                if i < i_stop + 1:
                    print (resu[key][str(i)]+ '\n')
                    i += 1
                else:
                    print ('done')
           

if __name__== "__main__":
    print ('\033[1m' + "Instructions: " + '\033[0m')
    print (" 1. Type recent search of choice \n 2. Type a colon sign \n 3. For certain hit, write number. \n For range of hits, write start and stop number with comma sign in between \n")
    print ('\033[1m' + "What hits would you like to see?" + '\033[0m')
    innumbers = input()
    findthehits(innumbers)
