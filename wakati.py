import pickle
import gzip

import os

import sys

import glob

import MeCab

import re

import random
if '--verb' in sys.argv:
  m = MeCab.Tagger('-Ochasen')
  files =  glob.glob('contents/*')
  random.shuffle(files)
  size = len(files)
  def _verb( text ):
    tmp =  []
    for verbs in [ line.split('\t') for line in m.parse( text ).strip().split('\n') ]:
      if verbs == ['EOS']:
        continue
      term = verbs[0]
      typed = verbs[-3]
      if '名詞' in typed:
        tmp.append( term ) 
    return tmp 
  for index, name in enumerate(files):
    if index%100 == 0:
      print('now iter', index, '/', size, name)
    save_name = 'wakati-verbs/' + name.split('/').pop()

    if os.path.exists(save_name) is True:
      continue
    c = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
    c['h1'] = _verb( c['h1'] )
    c['article'] = _verb( c['article'] )
    # commentはコメントの数のこと！
    #c['comment'] = _verb( c['comment'] )
    c['time'] = ['time@%s'%t for t in re.sub(r'([年|月|日])', r'\1 ', re.sub(r'\d\d:\d\d', '', c['time']) ).split() ]
    

    open(save_name, 'wb').write( gzip.compress(pickle.dumps(c))  )
    print(save_name)

if '--all' in sys.argv:
  m = MeCab.Tagger('-Owakati')
  files =  glob.glob('contents/*')
  size = len(files)
  for index, name in enumerate(files):
    if index%100 == 0:
      print('now iter', index, '/', size, name)
    save_name = 'wakati/' + name.split('/').pop()

    if os.path.exists(save_name) is True:
      continue
    c = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
    c['h1'] = m.parse( c['h1'] ).strip().split()
    c['article'] = m.parse( c['article'] ).strip().split()
    c['time'] = ['time@%s'%t for t in re.sub(r'([年|月|日])', r'\1 ', re.sub(r'\d\d:\d\d', '', c['time']) ).split() ]
    
    print( c )

    open(save_name, 'wb').write( gzip.compress(pickle.dumps(c))  )
    print(save_name)
 

