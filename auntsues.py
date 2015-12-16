import sys,os

sue_in = sys.argv[1]
sue_dict = {}
for line in open(sue_in).readlines():
  l_list = line.split(' ')
  for ind,i in enumerate(l_list):
    if(i!='Sue' and i[:-1].isalpha()):
      #print i
      if(not(l_list[1] in sue_dict)):
        sue_dict[l_list[1]]={}
      sue_dict[l_list[1]][i]= l_list[ind+1][:-1]

gift_dict = {'children:':'3','cats:':'7','samoyeds:':'2','pomeranians:':'3','akitas:':'0','vizslas:':'0','goldfish:':'5','trees:':'3','cars:':'2','perfumes:':'1'}
sue_num=0
max_count=0
for sue,traits in sue_dict.iteritems():
  sue_count=0
  for trait,val in traits.iteritems():
    if(trait=='cats:' or trait=='trees:'):
      if(val>gift_dict[trait]):
        sue_count+=1
      else:
        sue_count-=5
    elif(trait=='pomeranians:' or trait=='goldfish:'):
      if(val<gift_dict[trait]):
        sue_count+=1
      else:
        sue_count-=5
    else:
      if(val==gift_dict[trait]):
        sue_count+=1
      else:
        sue_count-=5
  #print sue,sue_count
  if(sue_count>max_count):
    sue_num=sue

print sue_num 
