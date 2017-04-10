import json,os,time
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
vocap=set()
fin={}
def process_category(arg):
    threads=20
    files=[]
    category_name=arg[0]
    category_files=arg[1]
    threads=arg=[2]
    for i in category_files:
        files.append([category_name,i])
    pool = ThreadPool(threads) 
    results = pool.map(process_subfile,files)
    a=set()
    for i in results:
        a=a.union(i)
    return a
def process_subfile(args):
    category_name=arg[0]
    file_name=args[1]
    d=set()
    try:
        with open(os.getcwd()+r'/input/jsons/train-multi.json','r') as file1:
            dp=file1.read()
            file1.close()
    except IOError as err:
        print err
    finally:
        bag=json.loads(dp)
    a=bag[category_name][file_name]    
    b=a.split()
    return set(b)
if __name__ == '__main__':
    start=time.time()
    print "Program started at: ",start
   # processes_limit=int(sys.argv[1])
   # threads=int(sys.argv[2])
    processes_limit=3
    threads=20
    print "Program started at: ",start
    vocap=set()
    fin={}
    try:
        with open(os.getcwd()+r'/input/jsons/train-multi.json','r') as file1:
            dp=file1.read()    
            file1.close()
        
    except IOError as err:
        print err
    finally:
        bag=json.loads(dp)
    lit=[]
    mlit=[]
    a=0
    for i in bag:
        lit2=[]
        for keys in bag[i]:
            lit2.append(keys)
        lit2=[i,lit2,threads]
        mlit.append(lit2)
    print len(mlit)
    p = Pool(processes=processes_limit)
    results=p.map(process_category, mlit)
    ans=set()
    for i in results:
        ans=ans.union(i)
    print ans
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start