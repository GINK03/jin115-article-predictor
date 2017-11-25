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
import random
import concurrent.futures 
if '--map1' in sys.argv:
  def _save_flag(link):
    save_name = 'flags/' + link
    open(save_name, 'w') 
  def _map1(arr):
    index, name = arr
    if index%100 == 0:
      print('now iter', index, name)
    try:
      for i in [1]:
        link = name.split('/').pop()
        save_name = 'contents/' + link
        if os.path.exists(save_name) is True: 
          continue
        if os.path.exists( 'flags/' + link ) is True:
          continue

        # remove #comment_list url
        if '#comment_list' in link:
          continue
        soup = bs4.BeautifulSoup( open(name).read() )
        h1 = soup.find('h1')
        if h1 is None:
          _save_flag(link)
          continue
        h1 = h1.text
        if h1 == '' or h1 == '404 Not Found':
          _save_flag(link)
          continue

        comment =  soup.find('a', {'title': 'Comment'})
        if comment is None:
          _save_flag(link)
          continue

        article = soup.find('div', {'class':'article_bodymore'})

        if article is None:
          _save_flag(link)
          continue

        time = soup.find('time', {'pubdate': 'pubdate'}).text
        contents = {}
        contents['h1'] = h1
        contents['comment'] = comment.text.replace('\n', '') 
        contents['article'] = re.sub(r'\n{1,}', ' ', article.text) 
        contents['time'] = time
        
        #print( contents )
        open(save_name, 'wb').write( gzip.compress(pickle.dumps(contents) ) )
        print('finished', link)
    except Exception as e:
      print('Deep Error',e )
  files =  glob.glob('../squid-config-dotfile/exmaple/htmls/*')
  random.shuffle(files)
  arrs = [(index, name) for index, name in enumerate(files)]
  
  with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
    exe.map( _map1, arrs)


