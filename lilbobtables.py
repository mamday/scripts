import sys
import numpy

in_file = sys.argv[1]
my_dict = {}
for line in open(in_file).readlines():
  text = line.split(' ')
  if(len(text)==3):
    my_dict[text[2].strip()]=text[0]
    #print 'Whee',text,my_dict[text[0]],text[0],text[2]
  elif(len(text)==5):
    my_dict[text[4].strip()]=text[:3]
    #print 'La',text,my_dict[text[4]]
  elif(len(text)==4):
    my_dict[text[3].strip()]=text[:2]
    #print 'Lee',text,text[3],my_dict[text[3]]
  else:
    pass
    #print 'What?',len(text),text[0],text
print my_dict['a']

def FindAll(node):
  first=my_dict[node]
  if(isinstance(first,str)):
    for i in my_dict.keys(): 
      if i==first:
        print 'Str Key',first,i
  else:
    for i in my_dict.keys(): 
      if i in first:
        print 'List Key',first,i

FindAll('a')
