import math,numpy
import sys,os

in_file = sys.argv[1]
global hen_list,boss_list
boss_list = [0,0,0,0]
for line in open(in_file).readlines():
 l1 = line.split()
 if('Hit' in line):
   boss_list[0]=int(l1[-1])
 if('Damage:' in line):
   boss_list[1]=int(l1[-1])

mag_dict={'MM':(53,4,0,1,0,0),'Drain':(73,2,2,1,0,0),'Shield':(113,0,0,6,7,0),'Poison':(173,3,0,6,0,0),'Recharge':(229,0,0,5,0,101)}

hen_list = [50,0,500,0]

print hen_list,boss_list

#I ended up doing this in my head. Since you MUST cast recharge, poison, and shield a certain number of times in order to have enough mana to both survive and do enough damage (it turns out to be 4xPoison and 3xRecharge in both cases, and 3xShield for 'Normal' and 4xShield for 'Hard' Mode), there are actually very few combinations that make sense (I tested ~3-4 solutions and got the answer after about ten minutes in all cases which turned out to require 2xMM in both cases for my test case). It seems like any coding algorithm will be far less efficient than common sense in this case...
