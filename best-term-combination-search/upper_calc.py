import os

import sys

import json

import math
# baselineの計算
os.system('lightgbm config=./pred.baseline.conf')

baseline = float( open('LightGBM_predict_result.txt').read().strip() )

# 探索的な予想の計算
os.system('lightgbm config=./pred.conf')

term_freq = json.loads( open('term_freq.json').read() )
cmerge = json.loads( open('count_merge.json').read() )

weights = []
for line in open('LightGBM_predict_result.txt'):
  line = line.strip()
  weights.append( math.exp( float(line) ) - math.exp( baseline ) )

merge_weight = {}
for weight, (count, merge) in zip(weights, cmerge):
  # rint( weight, count, merge )
  terms = tuple( merge )
  merge_weight[terms] = weight

for merge, weight in sorted(merge_weight.items(), key=lambda x:x[1]*-1):
  print( merge, weight)
