#!/usr/bin/env python3
import numpy
import pdb
import hcluster
import csv
import pickle
import pdb

def intersect(a,b):
    return list(set(a) & set(b))

def jcsimilarity(ne1,ne2,conveclist,docs):

  length = len(conveclist)


  temp_list = []
  jc_matrix=[]

  for i in range(length):
       for j in range(i+1):
          if i == j:
              temp_list.extend([0])
          else:
              temp_list.extend([round(float(len(set(conveclist[i]) & set(conveclist[j])))/float(len(set(conveclist[i]) | set( conveclist[j]))),3)])

       jc_matrix.append(temp_list)
       temp_list=[]    

  numpy.savetxt('jaccard2.txt',jc_matrix, delimiter=" ", fmt="%s" )       
  jcc_matrix = [[0],[10,0],[2,4,0],[3,6,5,0],[1,2,3,9,0],[6,7,8,20,2,0]]
  
 # print ('Enter hcluster')
  relations =  hcluster.hcluster(jc_matrix, conveclist)
 # print ('Exit hcluster')
  relations.sort()  
  if not relations:
      return
  relation = []
  fp = open('wordlist.pkl')
  wordlist = pickle.load(fp)
   
  inv_wordlist = {v : k for k, v in wordlist.items()}
  fp.close()

  fp = open('NamedEntity.pkl')
  ne = pickle.load(fp)
  inv_ne = {v : k for k , v in ne.items()}

  fp.close()
  prev = []
 # count = 0
  if (len(relations)) > 1:
     while len(relations) > 0 : 
         rel = relations.pop()
         if rel != prev:
             
           if prev != []:
                    try:
                      with open('Relation.csv', 'a') as myfile:
                         if len(prev) > 0:
                           writer = csv.writer(myfile, dialect='excel')
                           row = [inv_ne[ne1],inv_ne[ne2],r,docs]    # change inv_wordlist with relation
                           writer.writerow(row)
                    except IOError as ioe:
                         print('Error: ' + str(ioe))
                   #relation = []  
                   # count = 0
                     

           r = []
           prev = rel[:]
           while  len(rel) > 0:
             r.append(inv_wordlist[rel.pop()])
          #   relation.append(r) 
          #   count += 1
        # else:
         #  r = []
         #  prev = rel[:]
         #  while len(rel) > 0:
         #    r.append(inv_wordlist[rel.pop()])
         #    relation.append(r)
         #    count += 1




     try:
        with open('Relation.csv', 'a') as myfile:
          if len(prev) > 0 : 
            writer = csv.writer(myfile, dialect='excel')
            row = [inv_ne[ne1],inv_ne[ne2], r,docs]
            writer.writerow(row)
     except IOError as ioe:
         print('Error: ' + str(ioe))

