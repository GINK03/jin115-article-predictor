import glob

import pickle

import json

import gzip

import sys

import os

from collections import Counter

import math

import re

import random
if '--terms' in sys.argv:
  terms = set()
  for name in glob.glob('wakati/*'):
    c = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
    [ terms.add('comment@%s'%term) for term in c['comment'] ]
    [ terms.add('article@%s'%term) for term in c['article'] ]
    [ terms.add('%s'%term) for term in c['time'] ]
  open('temps/terms.json', 'w').write( json.dumps(list(terms), indent=2, ensure_ascii=False) )

  term_index = {}
  for index, term in enumerate(terms):
    term_index[term] = index 

  open('temps/term_index.json', 'w').write( json.dumps(term_index, indent=2, ensure_ascii=False) )

if '--sparse' in sys.argv:
  term_index = json.loads( open('temps/term_index.json').read() )
  ftrain = open('dataset.train', 'w')
  ftest  = open('dataset.test', 'w')
  for name in glob.glob('wakati/*'):
    # filter #comment_list's url
    if '#comment_list' in name: continue
    c = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )

    comment = int( re.search(r'（(\d{1,})）', c['comment']).group(1) )
    try:
      comment = math.log(comment)
    except Exception:
      continue
    print( comment )
    base = [ term_index['comment@%s'%term] for term in c['comment'] ]
    base.extend( [ term_index['article@%s'%term] for term in c['article'] ] )
    base.extend( [ term_index['%s'%term] for term in c['time'] ] )
     
    base = ' '.join( ['%d:%f'%(feat, math.log(freq+1)) for feat, freq in dict(Counter(base)).items()] )
    # print( c )
    if random.random() < 0.2:
      ftest.write( '%s %s'%(comment, base) + '\n')
    else:
      ftrain.write( '%s %s'%(comment, base) + '\n')
