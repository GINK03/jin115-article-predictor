import json

import sys

import re


term_index = json.loads( open('../temps/term_index.json').read() )
index_term = { index:term for term, index in term_index.items() }

usable_terms = []
for line in open('LightGBM_model.txt'):
  line = line.strip()
  if re.search(r'^Column_', line) is None:
    continue

  index = re.search(r'_(\d{1,})=', line).group(1)
  importance = re.search(r'=(\d{1,})',line).group(1)
  #print( index_term[int(index)], importance)
  usable_terms.append( index_term[int(index)] )

open('usable_terms.json', 'w').write( json.dumps(usable_terms, indent=2, ensure_ascii=False) )

