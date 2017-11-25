import json

import sys

import re


term_index = json.loads( open('temps/term_index.json').read() )
index_term = { index:term for term, index in term_index.items() }

if '--lightgbm' in sys.argv:
  for line in open('LightGBM_model.txt'):
    line = line.strip()
    if re.search(r'^Column_', line) is None:
      continue

    index = re.search(r'_(\d{1,})=', line).group(1)
    importance = re.search(r'=(\d{1,})',line).group(1)
    print( index_term[int(index)], importance)

if '--xgb' in sys.argv:
  feat_freq = {}
  for line in open('dump.txt'):
    line = line.strip()
    m = re.search(r'\[f(\d{1,})<', line)
    if m is None:
      continue
    feat = m.group(1)
    if feat_freq.get(feat) is None:
      feat_freq[feat] = 0
    feat_freq[feat] += 1
  for feat, freq in sorted( feat_freq.items(), key=lambda x:x[1]*-1):
    print(index_term[int(feat)], freq)
