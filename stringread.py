import sys

in_file = sys.argv[1]
lits=0
strs=0
tot=0

for line in open(in_file).readlines():
  strs+=len(line.encode('string_escape').replace('"','\\"'))
  lits+=len(line.decode('string_escape'))-3
  tot+=len(line)-1
  print line.decode('string_escape'),'la',line.encode('string-escape').replace('"','\\"'),len(line.encode('string_escape').replace('"','\\"')),len(line)-1 
print tot,lits,strs 
