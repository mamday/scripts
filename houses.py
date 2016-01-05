import sys,os

in_num = int(sys.argv[1])
in_elves = int(sys.argv[2])
house_dict = {}
for i in xrange(1,in_elves):
  for j in xrange(0,in_elves,i):
    #print [True for key,val in house_dict.iteritems() if(val>in_num)]
    if(not(True in [True for key,val in house_dict.iteritems() if val>in_num])):
      if(j==0):
        continue
      if(j in house_dict):
        #print i,j,house_dict[j],j*10
        house_dict[j]+=i*10
      else:
        #print i,j,j*10
        house_dict[j]=i*10
    else:
       break
print house_dict,[key for key,val in house_dict.iteritems() if(val>in_num)]
