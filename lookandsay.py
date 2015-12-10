import sys

in_file = sys.argv[1]
cur_str = ''
num_times = sys.argv[2]

#Look and Say
def LAndS(num_str):
  new_str = ''
  h_str = ''
  count=0
  ind=0
  #print 'Start',num_str
  for i in num_str:
    ind+=1
    if(h_str==''):
      h_str=i
    #print 'B',h_str,i,new_str
    if(not(i==h_str)):
      #print 'n',i,h_str
      new_str=new_str+str(count)+h_str
      count=0
    count+=1
    h_str=i
    if(ind==len(num_str)):
      #print 'H'
      new_str=new_str+str(count)+h_str
  #print 'Ans',new_str
  return new_str

#Get initial value,run first iteration
for line in open(in_file).readlines():
  in_str = line[:-1]
  cur_str = LAndS(in_str)

#Run other n-1 iterations
for i in xrange(0,int(num_times)-1):
  in_str = cur_str 
  print 'C',i,len(cur_str)
  cur_str = LAndS(in_str)

print 'E',len(cur_str) 
