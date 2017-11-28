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
from scipy.sparse import *
from scipy import *


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
print 'NE count',  n_ne



pickle.dump(named_entity, text_file)
text_file.close()

fp = open("wordlist.pkl","w")
pickle.dump(wordlist, fp)

fp.close()

print 'pickle files dumped ...'

contextvector=[]
#con_vec_mat=numpy.zeros((n_ne,n_ne), dtype=object)

con_vec_mat = csc_matrix( (n_ne,n_ne), dtype=uint16 ).todense()

#con_vec_mat = [[[] for i in range(3)] for i in range(10000)]
doc_mat=csc_matrix((n_ne,n_ne), dtype=uint16).todense()

filename = 'Relation.csv'
try:
    os.remove(filename)
except OSError:
    pass


flag = 'N'
count = 0
row=-1
max_row = -1
max_col = -1
col = -1
context=[]
level=0
vector = collections.OrderedDict()
text_format =[]
simplified = []
temp= 0
doc_idx = 0
doc_vector = collections.OrderedDict()
docid= 1
docNumber= [docid]

for sentences in open(inputfile):
    for terms in sentences.split():
         if pattern3.match(terms.lower()) and terms.lower() != 'the':
           #pdb.set_trace()
           word=terms.lower()
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
                  if con_vec_mat[row,col] ==0:
                     con_vec_mat[row,col] = level
                     vector[level]=[context]
                     simplified  
                     doc_mat[row,col] =  doc_idx
                     doc_vector[doc_idx] = [docid]
                     level = level + 1
                     doc_idx = doc_idx + 1
                  else:
                     temp = con_vec_mat[row,col]
                     vector[temp].append(context)
                     if docid not in doc_vector[doc_mat[row,col]]:
                         doc_vector[doc_mat[row,col]].append(docid)

               context = []
               if row > max_row:
                   max_row = row
               if col > max_col:
                   max_col = col
               continue
           elif flag == 'Y':
              if word in wordlist:                            
                 context.append(wordlist[word])   ## to print the context words use context.append(word)
              continue
    docid = docid+1
  
#print contextvector
#print con_vec_mat
print 'Context vector for NE generated.'

#numpy.savetxt('test.txt',con_vec_mat, delimiter=" ", fmt="%s" )
#text_file = open("output.txt", "w")

#filename = os.path.expanduser('~') + '\Desktop\input.txt'
#pdb.set_trace()

#filename = 'Relation.csv'
#try:
#    os.remove(filename)
#except OSError:
#    pass

for i in range(max_row):
       for j in  range(max_col):
            if vector[con_vec_mat[i,j]] != 0 and len(vector[con_vec_mat[i,j]]) > 1 :
                 #text_file.write( "%d -> %d: %s\n" %(i,j ,vector[con_vec_mat[i,j]]))
                 #if len(vector[con_vec_mat[i,j]]) > 1 :
                   jcsimilarity(i,j,vector[con_vec_mat[i,j]],doc_vector[doc_mat[i,j]]) 

os.remove('NamedEntity.pkl')
