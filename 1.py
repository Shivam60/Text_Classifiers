import os,string,json,time,multiprocessing,enchant,threading
from threading import Thread
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Process
words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)
bag={}
def process_file(t):
    t=[x for x in t]
    subfile=t[0]
    subfolder=t[1]
    path=t[2]
    try:
        with open(path+subfile,'r') as file1:
            doc=file1.read()
    except IOError as err:
        print "{0}".format(err)
    finally:
        file1.close()
    doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
    doc=" ".join([word.lower() for word in doc.split() if word not in stop and words.check(word) ])
    dq={}
    bag[str(subfile)]=doc
if __name__ == '__main__':
    start=time.time()
    print "Program started at: ",start
    a=['17536-178852', 'talk.politics.misc', '/home/shivam/Programing/Current_Projects/Text_Classifiers/input/train/talk.politics.misc/']
    th = Thread(target=process_file, args=(a,))
    th.start()
    th.join()
    print bag
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
