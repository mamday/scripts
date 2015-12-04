#! /usr/bin/env python 

import sys,hashlib
import multiprocessing
from multiprocessing import Process, Lock, Queue
my_string = sys.argv[1]
cur_hash = ''

def HashingThroughTheSnow(beg_int,end_int):
  for my_ints in xrange(beg_int,end_int):
    cur_hash = hashlib.md5(my_string+str(my_ints)).hexdigest()
    if(cur_hash[:6]=='000000'):
      print my_ints,cur_hash
      break
 
HashingThroughTheSnow(0,sys.maxint) 
