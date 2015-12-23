import sys,os

in_file = sys.argv[1]
in_str1=''
in_chems1 = {}
for line in open(in_file).readlines():
  if('=>' in line):
    if(line.split(' ')[0] in in_chems1):
      in_chems1[line.split(' ')[0]].append(line.split(' ')[2][:-1])
    else:
      in_chems1[line.split(' ')[0]]=[]
      in_chems1[line.split(' ')[0]].append(line.split(' ')[2][:-1])
  else:
    in_str1=line

def IterChems(in_chems,in_str):
  new_chems = {}
  for chem,reps in in_chems.iteritems():
    for lets in xrange(len(in_str)):
      if(len(in_str)>(lets+len(chem)) and in_str[lets:lets+len(chem)]==chem):
        for rep in reps:
          new_chems[in_str[:lets]+rep+in_str[lets+len(chem):]]=1
  return new_chems
new_chems1 = IterChems(in_chems1,in_str1)
print len(new_chems1) 
