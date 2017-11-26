import os

import glob

import bs4

import requests


r = requests.get('http://jin115.com/archives/52200128.html')
soup = bs4.BeautifulSoup(r.text)

article = soup.find('div', {'class':'article_bodymore'}).text
comment = soup.find('a', {'title': 'Comment'}).text
h1 = soup.find('h1').text

import MeCab

import re
m = MeCab.Tagger('-Owakati')

base = [ 'h1@%s'%term for term in m.parse(h1).strip().split() ]
base.extend( [ 'article@%s'%term for term in m.parse(article).strip().split() ] )
comment_num = re.search(r'\d{1,}', comment).group(0) 
print('comment num', comment_num )

from collections import Counter

import math

term_freq = {}
for term, freq in dict(Counter(base)).items():
	term_freq[term] = freq

import json

open('term_freq.json', 'w').write( json.dumps(term_freq, indent=2, ensure_ascii=False) )
