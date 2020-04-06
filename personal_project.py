from functools import reduce
import PyPDF4 as pidf
from nltk.corpus import stopwords
from collections import Counter as c
import time as t
import string as s
import nltk
from multiprocessing import Pool
import os
from nltk.corpus import words
import matplotlib.pyplot as plt
english_words=set(words.words())
stopwords=set(stopwords.words("english"))
punctuations=s.punctuation
whitespaces=s.whitespace

def is_not_digit(word):
    return any(i.isdigit() for i in word)

def preprocess(file):
    pdfFileObj=open(file,"rb")
    pdfreader=pidf.PdfFileReader(pdfFileObj)
    num_pages=pdfreader.numPages
    text1=''
    for i in range(num_pages):
        pageObj=pdfreader.getPage(i)
        text1+=pageObj.extractText()

    if text1:
        tokens=nltk.word_tokenize(text1)
        keywords=keywords=' '.join(word for word in tokens if word not in punctuations and word not in stopwords and word not in whitespaces and not is_not_digit(word) and len(word)>3 and word in english_words)
        if keywords:
            return keywords
    else:

        return text1

def mapper(paragraphs):
    my_counter=c()
    for words in paragraphs.split(" "):
        if words:
            my_counter[words]+=1
    return my_counter


def reduce_function (x,y):
    return c(x)+c(y)


def plot_most_freq_dist(final_result):
    plt.bar([x[0] for x in final_result.most_common(5)],[x[1] for x in final_result.most_common(5)])
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.title("PDF WORD SUMMARY")
    plt.legend()
    plt.show()

if __name__=='__main__':
    required_words_from_each_pdf=[]
    for pdfs in os.listdir("C:/Users/3301/Desktop/Pdfs"):
        pdfs="C:/Users/3301/Desktop/Pdfs/"+pdfs
        rv=preprocess(pdfs)
        if rv:
            required_words_from_each_pdf.append(rv)
    with Pool(3) as p:
        result=p.map(mapper,required_words_from_each_pdf)
        final_result=reduce(reduce_function,result)

    plot_most_freq_dist(final_result)
