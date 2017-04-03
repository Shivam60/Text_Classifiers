from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfTransformer
import os
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import os
from sklearn.pipeline import Pipeline

wdtr=os.getcwd()+"/train"
a=load_files(wdtr)
text_clf = Pipeline([('vect', CountVectorizer(decode_error=u'ignore')),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])
text_clf = text_clf.fit(a.data, a.target)
cltrn= ['God is love', 'OpenGL on the GPU is fast']
for i in text_clf.predict(cltrn):
	print a.target_names[i] 

import numpy as np
wdtr=os.getcwd()+"/test"
b=load_files(wdtr)

docs_test = b.data
predicted = text_clf.predict(docs_test)
print np.mean(predicted == b.target)            

