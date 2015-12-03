#! /usr/bin/env python

import sys,os

my_in = sys.argv[1]
in_str = ''
for line in open(my_in).readlines():
  in_str = str(line)

countew = 0
countns = 0
rcountew = 0
rcountns = 0
vis_dict = {}
vis_dict[(0,0)]=1
odd_bool = True
for dir_char in in_str:
  if(dir_char=='>'):
    if(odd_bool):
      countew+=1
    else:
      rcountew+=1
  if(dir_char=='<'):
    if(odd_bool):
      countew-=1
    else:
      rcountew-=1
  if(dir_char=='^'):
    if(odd_bool):
      countns+=1
    else:
      rcountns+=1
  if(dir_char=='v'):
    if(odd_bool):
      countns-=1
    else:
      rcountns-=1
  if(odd_bool):
    if((countew,countns) in vis_dict):
      vis_dict[(countew,countns)]+=1
    else:
      vis_dict[(countew,countns)]=1
  else:
    if((rcountew,rcountns) in vis_dict):
      vis_dict[(countew,countns)]+=1
    else:
      vis_dict[(rcountew,rcountns)]=1
  if(odd_bool): odd_bool=False
  else: odd_bool=True
print vis_dict,len(vis_dict) 
