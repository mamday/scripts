#! /usr/bin/env python

import sys
import numpy

in_file = sys.argv[1]

light_arr = numpy.zeros((1000,1000),dtype=bool)
#light_arr = numpy.zeros((3,3),dtype=bool)

for line in open(in_file).readlines():
  text = line.split(' ')
  #print 'Text',text,str(text[0])
  if((str(text[0])=='turn') and (str(text[1])=='on')):
    #print 'Here On',text[1]
    first_dir = text[2].split(',')
    last_dir = text[4].split(',')
    first_one = int(first_dir[0])
    first_two = int(first_dir[1])
    last_one = int(last_dir[0])
    last_two = int(last_dir[1])
    light_arr[first_one:(last_one +1),first_two:(last_two+1)]=1 
    #print 'On',light_arr,light_arr[first_one:(last_one +1),first_two:(last_two+1)],first_one,first_two,last_one,last_two
  elif((str(text[0])=='turn') and (str(text[1])=='off')):
    #print 'Here Off',text[1]
    first_dir = text[2].split(',')
    last_dir = text[4].split(',')
    first_one = int(first_dir[0])
    first_two = int(first_dir[1])
    last_one = int(last_dir[0])
    last_two = int(last_dir[1])
    light_arr[first_one:(last_one +1),first_two:(last_two+1)]=0
    #print 'Off',light_arr,light_arr[first_one:(last_one +1),first_two:(last_two+1)],first_one,first_two,last_one,last_two
  elif(str(text[0])=='toggle'):
    first_dir = text[1].split(',')
    last_dir = text[3].split(',')
    first_one = int(first_dir[0])
    first_two = int(first_dir[1])
    last_one = int(last_dir[0])
    last_two = int(last_dir[1])
    light_arr[first_one:(last_one +1),first_two:(last_two+1)]-=1
    #print 'Tog',light_arr,light_arr[first_one:(last_one +1),first_two:(last_two+1)],first_one,first_two,last_one,last_two
print light_arr,len(light_arr[light_arr]) 
