import os
import sys

import glob

import bs4

import MeCab

import re

import plyvel

import pickle
import gzip
import sys

import concurrent.futures 
if '--map1' in sys.argv:

  def _map1(name):
    for i in [1]:
      link = name.split('/').pop()
      save_name = 'contents/' + link
      if os.path.exists(save_name) is True: 
        continue
      soup = bs4.BeautifulSoup( open(name).read() )
      h1 = soup.find('h1')
      if h1 is None:
        continue
      h1 = h1.text
      if h1 == '' or h1 == '404 Not Found':
        continue

      comment =  soup.find('a', {'title': 'Comment'})
      if comment is None:
        continue

      article = soup.find('div', {'class':'article_bodymore'})

      if article is None:
        continue
      contents = {}
      contents['h1'] = h1
      contents['comment'] = comment.text.replace('\n', '') 
      contents['article'] = re.sub(r'\n{1,}', ' ', article.text) 
      
      open(save_name, 'wb').write( gzip.compress(pickle.dumps(contents) ) )
      print('finished', link)
  
  names = [name for name in glob.glob('../squid-config-dotfile/exmaple/htmls/*')]
  with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
    exe.map( _map1, names)


