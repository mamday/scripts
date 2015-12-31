import sys
import numpy

#Get input information about circuit and store in my dictionary my_dict
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

#Final values
global fin_dict
fin_dict={}

#Get initial numbers 
def FindNums(in_dict):
  global fin_dict
  num_list = []
  for key,entry in in_dict.iteritems():
    if(isinstance(entry,str)):
      if entry.isdigit():
        num_list.append(key)
        fin_dict[key]=entry
  return num_list

n_list = FindNums(my_dict)
print n_list
#Get numbers for instructions containing nm
def IterNums(nm,nm_list,i_dict):
  global fin_dict
  for key,entry in i_dict.iteritems():
    #print 'Beg',key,entry
    if(key in fin_dict):
      #print 'F',key
      continue 
    elif(not(isinstance(entry,str))):
      if nm in entry:
        if('AND' in entry): 
          if((entry[0].isdigit() or (entry[0] in nm_list)) and (entry[2].isdigit() or (entry[2] in nm_list))):
            if(entry[0].isdigit() and not(entry[2].isdigit())):
              fin_dict[key]=int(entry[0]) & int(fin_dict[entry[2]]) 
            elif(entry[2].isdigit() and not(entry[0].isdigit())):
              fin_dict[key]=int(entry[2]) & int(fin_dict[entry[0]]) 
            elif(not(entry[0].isdigit()) and not(entry[2].isdigit())):
              fin_dict[key]=int(fin_dict[entry[2]]) & int(fin_dict[entry[0]]) 
            elif(entry[0].isdigit() and entry[2].isdigit()):
              fin_dict[key]=int(entry[0]) & int(entry[2]) 
            #print 'A',fin_dict
        elif('OR' in entry): 
          if((entry[0].isdigit() or (entry[0] in nm_list)) and (entry[2].isdigit() or (entry[2] in nm_list))):
            if(entry[0].isdigit() and not(entry[2].isdigit())):
              fin_dict[key]=int(entry[0]) | int(fin_dict[entry[2]]) 
            elif(entry[2].isdigit() and not(entry[0].isdigit())):
              fin_dict[key]=int(entry[2]) | int(fin_dict[entry[0]]) 
            elif(not(entry[0].isdigit()) and not(entry[2].isdigit())):
              fin_dict[key]=int(fin_dict[entry[2]]) | int(fin_dict[entry[0]]) 
            elif(entry[0].isdigit() and entry[2].isdigit()):
              fin_dict[key]=int(entry[0]) | int(entry[2]) 
            #print 'O',fin_dict
        elif('LSHIFT' in entry): 
          if((entry[0].isdigit() or (entry[0] in nm_list)) and (entry[2].isdigit() or (entry[2] in nm_list))):
            if(entry[0].isdigit() and not(entry[2].isdigit())):
              fin_dict[key]=int(entry[0]) << int(fin_dict[entry[2]]) 
            elif(entry[2].isdigit() and not(entry[0].isdigit())):
              fin_dict[key]=int(fin_dict[entry[0]]) << int(entry[2]) 
            elif(not(entry[0].isdigit()) and not(entry[2].isdigit())):
              fin_dict[key]=int(fin_dict[entry[0]]) << int(fin_dict[entry[2]]) 
            elif(entry[0].isdigit() and entry[2].isdigit()):
              fin_dict[key]=int(entry[0]) << int(entry[2]) 
            #print 'L',fin_dict
        elif('RSHIFT' in entry): 
          if((entry[0].isdigit() or (entry[0] in nm_list)) and (entry[2].isdigit() or (entry[2] in nm_list))):
            if(entry[0].isdigit() and not(entry[2].isdigit())):
              fin_dict[key]=int(entry[0]) >> int(fin_dict[entry[2]]) 
            elif(entry[2].isdigit() and not(entry[0].isdigit())):
              fin_dict[key]= int(fin_dict[entry[0]]) >> int(entry[2]) 
            elif(not(entry[0].isdigit()) and not(entry[2].isdigit())):
              fin_dict[key]= int(fin_dict[entry[0]]) >> int(fin_dict[entry[2]]) 
            elif(entry[0].isdigit() and entry[2].isdigit()):
              fin_dict[key]=int(entry[0]) >> int(entry[2]) 
            #print 'R',fin_dict
        elif('NOT' in entry): 
          if(entry[1].isdigit()):
            fin_dict[key]=~int(entry[1]) & 0xFFFF
          else:
            fin_dict[key]=~int(fin_dict[entry[1]]) & 0xFFFF
          #print 'N',fin_dict
    else:
      if(entry.isdigit()):
        print 'D',entry
        pass
      else:
        if(entry==nm):
          fin_dict[key]=fin_dict[nm]
          print 'SY',fin_dict,entry
        else:
          print 'SN',entry
          pass

#Iterate over all instructions
while(len(fin_dict) != len(my_dict)):
  for nm in n_list:
    IterNums(nm,n_list,my_dict)
  #print 'Loop',fin_dict
  n_list = fin_dict.keys()

print fin_dict['b'],fin_dict['a']
