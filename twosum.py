# /usr/bin/env python

import numpy
import os,sys
import math

mfile = sys.argv[1]
my_hash = {}
for line in open(mfile).readlines():
  my_hash[int(line)] = {} 

count = 0
counter = 0
my_range = {key: None for key in numpy.linspace(-10000,10000,20001)}
for key,mdict in my_hash.iteritems():
  counter+=1
  for val,ent in my_range.iteritems():
      if((key==(val-key)) or my_range[val]!=None):
        continue
      if(int(val-key) in my_hash):
          #print key,val-key,my_hash[val-key]
          if(not((int(key) in my_hash) and (int(val-key) in my_hash[int(key)]))):
            if(not int(key) in my_hash[int(val-key)]):
              count+=1
              my_hash[int(key)][int(val-key)]=1
              my_range[val]=1
              print len(my_hash),counter 
              #print 'Here',int(val-key),int(key),len(my_hash[(val-key)])
              #print val,key,val-key 

print 'Done',count 
