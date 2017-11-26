import json

import os


import sys


term_freq = json.loads( open('term_freq.json').read() )

terms = json.loads( open('usable_terms.json').read() )

count_merge = {}
import random
for i in range(100000):
  merge = [ random.choice(terms) for j in range(3) ]
  count_merge[i] = merge

term_index = json.loads( open('../temps/term_index.json').read() )
import copy
import math

# base
open('baseline.dat', 'w').write( '0.0 ' + ' '.join(  [ '%d:%f'%(term_index[term], math.log(freq+1)) for term, freq in term_freq.items() if term_index.get(term) is not None ]  ) )


for count, merge in sorted( count_merge.items(), key=lambda x:x[0]):
  temp = copy.copy(term_freq)
  for term in merge:
    if temp.get(term) is None:
      temp[term] = 0.0
    temp[term] += 1

  temp = { term:math.log(freq+1) for term, freq in temp.items() }

  
  formula = ' '.join( ['%d:%f'%(term_index[term], freq) for term, freq in sorted(temp.items(), key=lambda x:x[0]) if term_index.get(term) is not None] )
  print( '0 ' + formula ) 

open('count_merge.json', 'w').write( json.dumps( sorted( count_merge.items(), key=lambda x:x[0]), indent=2, ensure_ascii=False ) )
