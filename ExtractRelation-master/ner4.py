#!/usr/bin/env python3

import os
import pdb
import re
import collections
import nltk
import numpy
import json
import codecs
import sys
from jcc import *
from nltk.corpus import stopwords
import pickle
reload(sys)
sys.setdefaultencoding('utf8')

##f = codecs.open("bigfile.txt", "r", "utf-8")
##sample = f.read()
if len(sys.argv)-1 == 1:
   inputfile = sys.argv[1]
else:
  sys.exit('Wrong number of args') 
with open (inputfile,'r') as f:
#with open ('busitechent.txt', 'r') as f:
   sample = f.read()
   sample.decode('cp1252').encode('utf-8')

###### ---- finding named entities starts
print 'Tokenizing document'
sentences = nltk.sent_tokenize(sample)
stop = stopwords.words('english')
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences ]
intermediate_sentences = [ [word for word in sentence if word not in stop]  for sentence in tokenized_sentences]

tagged_sentences = [ nltk.pos_tag(sen) for sen in intermediate_sentences ]

chunked_sentences =   nltk.ne_chunk_sents(tagged_sentences, binary=True)

named_entity=collections.OrderedDict(); 
wordlist = collections.OrderedDict()
n_ne = 0
prev1= ''
prev2=''
counter = 1
n_words = 0 
wl_flag = 'N'
#print tagged_sentences
print 'Tagged sentences found ...'

#pdb.set_trace()

for s in tagged_sentences:
   for terms in s:
       
       term=terms[0].lower()
       pattern = re.compile(r'[N]\w*')  ### Use N and J if we need adjectives as well. N alone will account for nouns of all forms
       pattern2 = re.compile(r'[N]\w*')
       pattern3 = re.compile(r'[a-z.]+') 

       if pattern.match(terms[1]) and pattern3.match(term):
                if term not in wordlist : 
                   named_entity[term]= n_ne
                   wordlist[term] = counter
                   n_ne = n_ne + 1
                   counter= counter+1
                   
       else:
             if pattern3.match(term) and term not in wordlist :
                wordlist[term]=counter
                counter = counter+ 1     

            
old = -1
ne_value = []
n_context_words=[]      ## this list contains the count of context words between each NE pair
print 'Named Entities extracted ...'

text_file = open("NamedEntity.pkl",'w')



pickle.dump(named_entity, text_file)
text_file.close()

fp = open("wordlist.pkl","w")
pickle.dump(wordlist, fp)

fp.close()

print 'pickle files dumped ...'

contextvector=[]
con_vec_mat=numpy.zeros((n_ne,n_ne), dtype=object)

flag = 'N'
count = 0
row=-1
max_row = -1
max_col = -1
col = -1
context=[]
text_format =[]
simplified = []
for sentences in tagged_sentences:
    for terms in sentences:
         if pattern3.match(terms[0].lower()) and terms[0].lower() != 'the':
           #pdb.set_trace()
           word=terms[0].lower()
           if word == '.':
              if context:
                 context = []
              flag = 'N' 
           elif  word in  named_entity:
               flag = 'Y'

               if word in named_entity and row < 0:
                   row = 0 
                   col = int(named_entity[word])
               elif word in named_entity and row >= 0:
                   row = col
                   col  = int(named_entity[word])
                
               if context:
                  contextvector.append(context)
                  #print (row,':',col)
                  if con_vec_mat[row][col] ==0:
                     con_vec_mat[row][col] = [context]
                     simplified  
                  else:
                     con_vec_mat[row][col].extend([context])
               context = []
               if row > max_row:
                   max_row = row
               if col > max_col:
                   max_col = col
               continue
           elif flag == 'Y':
               
               context.append(wordlist[word])   ## to print the context words use context.append(word)
#print contextvector
#print con_vec_mat
print 'Context vector for NE generated.'

numpy.savetxt('test.txt',con_vec_mat, delimiter=" ", fmt="%s" )
text_file = open("output.txt", "w")

#filename = os.path.expanduser('~') + '\Desktop\input.txt'
#pdb.set_trace()
filename = 'Relation.csv'
try:
    os.remove(filename)
except OSError:
    pass


for i in range(max_row):
       for j in  range(max_col):
            if con_vec_mat[i][j] != 0:
                 text_file.write( "%d -> %d: %s\n" %(i,j ,con_vec_mat[i][j]))
                 if len(con_vec_mat[i][j]) > 1 :
                     jcsimilarity(i,j,con_vec_mat[i][j]) 

