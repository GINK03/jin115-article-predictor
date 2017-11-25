import pickle
import gzip

import os

import sys

import glob

import MeCab

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
  #print( c )

  open(save_name, 'wb').write( gzip.compress(pickle.dumps(c))  )
  print(save_name)
 

