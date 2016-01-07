import sys,os

in_num = int(sys.argv[1])
#in_elves = int(sys.argv[2])
house_dict = {}
for i in xrange(1,(in_num/10)+1):
  house_dict[i]=0

for j in xrange(1,in_num/10):
  print j 
  for i in xrange(j,in_num/10,j):
    #print [True for key,val in house_dict.iteritems() if(val>in_num)]
    #print 'Test',house_dict
    #if(not(True in [True for key,val in house_dict.iteritems() if val>=in_num])):
      if(i==0):
        continue
      house_dict[i]+=j*10
      #print j,i,j*10
    #else:
    #  break
#print house_dict,[key for key,val in house_dict.iteritems() if(val>=in_num)]
print [key for key,val in house_dict.iteritems() if(val>=in_num)]
