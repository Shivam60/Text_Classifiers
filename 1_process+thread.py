import threading,os,string,json,time,multiprocessing,enchant,sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)
def process_folder(arg):
    files=[]
    path=arg[0]
    threads=int(arg[1])
    folder_name=path.split('/')
    folder_name=folder_name[len(folder_name)-2]
    d={}
    for i in os.listdir(path):
        files.append(path+i)
    pool = ThreadPool(threads) 
    results = pool.map(process_file,files)
    a={}
    for i in results:
        a.update(i)
    d[folder_name]=a
    print folder_name,len(d[folder_name])
    return d
def process_file(filename):
    d={}
    file_name=filename.split('/')
    file_name=file_name[len(file_name)-1]
    try:
        with open(filename,'r') as file1:
            doc=file1.read()
    except IOError as err:
        print err
    finally:
        file1.close()
    doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
    doc=" ".join([k.lower() for k in doc.split()])
    doc=" ".join([word.lower() for word in doc.split() if word not in stop and words.check(word)])
    d[file_name]=doc
    return d

if __name__ == '__main__':
    start=time.time()
    processes_limit=int(sys.argv[1])
    threads=int(sys.argv[2])
    print "Program started at: ",start
    print "Number of Processors used: ", processes_limit
    print "Number of Threads used: ", threads
    cwd=os.getcwd()
    train=cwd+r"/input/train/"
    categories=os.listdir(train)
    itter=[]
    for i in range(0,len(categories)):
        itter.append([train+categories[i]+r'/',threads])
    p = Pool(processes=processes_limit)
    results=p.map(process_folder, itter)
    a={}
    for i in results:
        a.update(i)

    try:
        with open(os.getcwd()+r'/input/jsons/multi-threaded.json','w') as file1:
            bag=json.dumps(a, sort_keys=True, indent=4, separators=(',', ': '))
            file1.write(bag)
    except IOError as err: 
        print "{0}".format(err)
    finally:
        file1.close()
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
    sys.exit(end-start)