import time
start=time.time()
print "Program started at: ",start
a=[1, 2, 3]
for i in a:
    b=i
    b1=i**7
    b2=i**8
    b3=i**9
    k=1
    for j in range(1,b1):
        k=k*j 
    print k
    for j in range(1,b2):
        k=k*j
    print k
    for j in range(1,b3):
        k=k*j
    print k
end=time.time()
print "Program ended at: ",end
print "Total Time to process: ",end-start