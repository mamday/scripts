import sys,os
import numpy,math

boss_stats = sys.argv[1]
start_hp = int(sys.argv[2])
boss_dict = {'hp':0,'dam':0,'arm':0}
hc_dict = {'hp':0,'dam':0,'arm':0}
#Get boss stats
for line in open(boss_stats).readlines():
  info = line.split(' ')
  if('Hit' in info):
    boss_dict['hp']=int(info[-1])
  if('Damage:' in info):
    boss_dict['dam']=int(info[-1])
  if('Armor:' in info):
    boss_dict['arm']=int(info[-1])

hc_dict['hp']=start_hp

#Gear stats
gear_dict = {'Weapons':[(8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0)],'Armor':[(12,0,1),(31,0,2),(53,0,3),(75,0,4),(102,0,5)],'Rings':[(20,0,1),(25,1,0),(40,0,2),(50,2,0),(80,0,3),(100,3,0)]}

w_ind=0
a_ind=0
r_ind=0
r_ind1=1

def IncWeapon(ind):
    hc_dict['dam']+=gear_dict['Weapons'][ind][1]

def IncArmor(ind):
    hc_dict['arm']+=gear_dict['Armor'][ind][2]

def IncRing(ind):
  hc_dict['dam']+=gear_dict['Rings'][ind][1]
  hc_dict['arm']+=gear_dict['Rings'][ind][2]

global boss_dead

def FightBoss():
  global boss_dead
  hc_hp = hc_dict['hp']
  boss_hp = boss_dict['hp']
  #print hc_hp,boss_hp,hc_dict,boss_dict,boss_dead
  while(hc_hp>0):
#Henry attacks boss
    if(boss_dict['arm']<hc_dict['dam']):
      boss_hp-=(hc_dict['dam']-boss_dict['arm'])
    else:
      boss_hp-=1
    if(boss_hp<=0):
      boss_dead=True
#Boss attacks Henry
    if(hc_dict['arm']<boss_dict['dam']):
      hc_hp-=(boss_dict['dam']-hc_dict['arm'])
    else:
      hc_hp-=1
    #print hc_hp,boss_hp,hc_dict,boss_dict,boss_dead

low_prices = []
#Try without armor or rings (and save cheapest prices)
boss_dead=False
while(boss_dead!='Fail'):
  hc_dict = {'hp':start_hp,'dam':0,'arm':0}
  IncWeapon(w_ind)
  FightBoss()
  if(not(boss_dead)):
    low_prices.append(gear_dict['Weapons'][w_ind][0])
    boss_dead=False
#Update indexes
  if((w_ind+1)==len(gear_dict['Weapons'])):
    boss_dead='Fail'
  else:
    w_ind+=1
  if(len(low_prices)>0):
    print 'W',len(low_prices),max(low_prices),boss_dead

r_ind=0
r_ind1=1
w_ind=0
#Try without armor and two rings (and save cheapest prices)
boss_dead=False
while(boss_dead!='Fail'):
  hc_dict = {'hp':start_hp,'dam':0,'arm':0}
  IncWeapon(w_ind)
  IncRing(r_ind)
  IncRing(r_ind1)
  FightBoss()
  if(not(boss_dead)):
    low_prices.append(gear_dict['Weapons'][w_ind][0]+gear_dict['Rings'][r_ind][0]+gear_dict['Rings'][r_ind1][0])
    boss_dead=False
#Update indexes
  if(w_ind+1==len(gear_dict['Weapons'])):
    if(r_ind+2==len(gear_dict['Rings'])):
      boss_dead='Fail' 
    elif(r_ind1+1<len(gear_dict['Rings'])):
      r_ind1+=1
    else:
      r_ind+=1
      r_ind1=r_ind+1
  elif(r_ind+2==len(gear_dict['Rings'])):
    if(w_ind+1==len(gear_dict['Weapons'])):
      boss_dead='Fail' 
    else: 
      w_ind+=1
      r_ind=0
      r_ind1=1
  elif(r_ind1+1<len(gear_dict['Rings'])):
    r_ind1+=1
  else:
    r_ind+=1
    r_ind1=r_ind+1
  if(len(low_prices)>0):
    print 'RW',len(low_prices),max(low_prices),boss_dead

w_ind=0
r_ind=0
boss_dead=False
#Try without armor and one ring (and save cheapest prices)
while(boss_dead!='Fail'):
  #print 'RW1',w_ind,r_ind
  hc_dict = {'hp':start_hp,'dam':0,'arm':0}
  IncWeapon(w_ind)
  IncRing(r_ind)
  FightBoss()
  if(not(boss_dead)):
    low_prices.append(gear_dict['Rings'][r_ind][0]+gear_dict['Weapons'][w_ind][0])
    boss_dead=False
#Update indexes
  if((w_ind+1)==len(gear_dict['Weapons'])):
    if((r_ind+1)==len(gear_dict['Rings'])):
      boss_dead='Fail'
    else:
      r_ind+=1
      w_ind=0
  else:
    w_ind+=1
  if(len(low_prices)>0):
    print 'WR1',len(low_prices),max(low_prices),boss_dead

w_ind=0
a_ind=0
boss_dead=False
#Try without rings (and save cheapest price)
while(boss_dead!='Fail'):
  hc_dict = {'hp':start_hp,'dam':0,'arm':0}
  IncWeapon(w_ind)
  IncArmor(a_ind)
  FightBoss()
  if(not(boss_dead)):
    low_prices.append(gear_dict['Armor'][a_ind][0]+gear_dict['Weapons'][w_ind][0])
    boss_dead=False
#Update indexes
  if((w_ind+1)==len(gear_dict['Weapons'])):
    if((a_ind+1)==len(gear_dict['Armor'])):
      boss_dead='Fail'
    else:
      a_ind+=1
      w_ind=0
  else:
    w_ind+=1
  if(len(low_prices)>0):
    print 'WA',len(low_prices),max(low_prices),boss_dead

w_ind=0
a_ind=0
r_ind=0
boss_dead=False
#Try with everything (but only 1 ring) (and save cheapest price)
while(boss_dead!='Fail'):
  #print 'All',w_ind,a_ind,r_ind
  hc_dict = {'hp':start_hp,'dam':0,'arm':0}
  IncWeapon(w_ind)
  IncArmor(a_ind)
  IncRing(r_ind)
  FightBoss()
  if(not(boss_dead)):
    low_prices.append(gear_dict['Rings'][r_ind][0]+gear_dict['Armor'][a_ind][0]+gear_dict['Weapons'][w_ind][0])
    boss_dead=False
#Update indexes
  if((w_ind+1)==len(gear_dict['Weapons'])):
    if((a_ind+1)==len(gear_dict['Armor'])):
      if((r_ind+1)==len(gear_dict['Rings'])):
        boss_dead='Fail'
      else:
        r_ind+=1
        a_ind=0
        w_ind=0
    else:
      a_ind+=1
      w_ind=0
  else:
    w_ind+=1
  if(len(low_prices)>0):
    print 'All',len(low_prices),max(low_prices),boss_dead

#Try with everything (with 2 rings) (and save cheapest price)
w_ind=0
a_ind=0
r_ind=0
r_ind1=1
boss_dead=False
while(boss_dead!='Fail'):
  hc_dict = {'hp':start_hp,'dam':0,'arm':0}
  #print 'All2',a_ind,w_ind,r_ind,r_ind1
  IncWeapon(w_ind)
  IncWeapon(a_ind)
  IncRing(r_ind)
  IncRing(r_ind1)
  FightBoss()
  if(not(boss_dead)):
    low_prices.append(gear_dict['Armor'][a_ind][0]+gear_dict['Weapons'][w_ind][0]+gear_dict['Rings'][r_ind][0]+gear_dict['Rings'][r_ind1][0])
    boss_dead=False
#Update indexes
  if(a_ind+1==len(gear_dict['Armor'])):
    if(w_ind+1==len(gear_dict['Weapons'])):
      if(r_ind+2==len(gear_dict['Rings'])):
        boss_dead='Fail' 
      elif(r_ind1+1<len(gear_dict['Rings'])):
        r_ind1+=1
      else:
        r_ind+=1
        r_ind1=r_ind+1
    else:
      if(r_ind+2==len(gear_dict['Rings'])):
        w_ind+=1
        a_ind=0
        r_ind=0
        r_ind1=1
      elif(r_ind1+1<len(gear_dict['Rings'])):
        r_ind1+=1
        a_ind=0
      else:
        a_ind=0
        r_ind+=1
        r_ind1=r_ind+1
  else:
    a_ind+=1
  if(len(low_prices)>0):
    print 'All2',len(low_prices),max(low_prices),boss_dead

