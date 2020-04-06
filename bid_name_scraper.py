import csv
import email
import nltk
import os
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import RegexpTokenizer
import time as t
mytokenizer=RegexpTokenizer('\w+')

def select_bid_names(fnames):
    with open(fnames) as f:
        try:
            a=[key[1] for key in email.message_from_string(f.read()).items() if key[0]=="Subject" ]
        except:
            return ''
        return a[0] if a else ''

def get_named_entity(subjects):
    for sentences in subjects:
        all_valid_subject=[]
        if sentences:
            words=mytokenizer.tokenize(sentences)
            tagged=nltk.pos_tag(words)
            namedEnt=nltk.ne_chunk(tagged,binary=True)
            for tuples in namedEnt:
                try:
                    if tuples[1]=="NNP"or tuples[1]=="NNS" or tuples[1]=="NC":
                        if type(tuples[0]=='str'):
                            all_valid_subject.append(tuples[0])
                        
                except:
                        for items in tuples[0]:
                            if items=="Fwd" or items=="Request" or items=="NNP" or items=="Bid" or items=="NN" or items=="JJ":
                                pass
                            else:
                                all_valid_subject.append(items)
                                
            return[' '.join(x for x in  all_valid_subject),1]
        else:
            return None


            
def write_in_csv(rows):
     with open("C:/Users/3301/Desktop/Files/bid_names.csv","a+") as my_csv_writer:
        writer=csv.writer(my_csv_writer)
        writer.writerow(rows)


if __name__=='__main__':
    fieldnames=["Bid_Names","Labels"]
    with open("C:/Users/3301/Desktop/Files/bid_names.csv","w") as my_csv_writer:
        writer=csv.DictWriter(my_csv_writer,fieldnames=fieldnames)
        writer.writeheader()

    subjects,csvwriter=[],[]
    for fnames in os.listdir('C:/Users/3301/Desktop/Files/Test_Data'):
        fnames='C:/Users/3301/Desktop/Files/Test_Data/'+ fnames
        subjects.append(select_bid_names(fnames))
        rv=get_named_entity(subjects)
        if rv and rv[0]:
            csvwriter.append(rv)
        subjects.pop(0)
    for rows in csvwriter:
        write_in_csv(rows)