import json

import os


import sys


term_freq = json.loads( open('term_freq.json').read() )

terms = json.loads( open('usable_terms.json').read() )

count = 0
count_merge = {}
for i in range(len(terms)):
  for j in range(len(terms)):
    for k in range(len(terms)):
      merge = [terms[i], terms[j], terms[k]] 
      count_merge[count] = merge
      count+=1

term_index = json.loads( open('../temps/term_index.json').read() )

import copy
for count, merge in count_merge.items():
  temp = copy.copy(term_freq)
  for term in merge:
    temp[term] += 1

  temp = { term:math.log(freq+1) for term, freq in copy.copy(temp.items())  }

  formula = ' '.join( ['%d:%f'%(term_index[term], freq) for term, freq in temp.items()] )
  print( '0.0 ' + formula ) 

