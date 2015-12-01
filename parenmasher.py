#! /usr/bin/env python

import sys
import math

in_file = sys.argv[1]
santa_text = ''
for line in open(in_file).readlines():
  santa_text = line
count=0
count1=0
for i in santa_text:
  count1+=1
  if(i=='('):
    count+=1  
  if(i==')'):
    count-=1  
  if(count<0):
    print count1
    break
print count  
