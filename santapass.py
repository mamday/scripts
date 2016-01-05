import sys,os
import math
in_pass1 = sys.argv[1]

global r_alphabet,s_alphabet,str_lis
r_alphabet = 'abcdefghijklmnopqrstuvwxyz'
s_alphabet = 'abcdefghjkmnpqrstuvwxyz'
str_lis = [0,0,0,0,0,0,0,0]
#Algorithm to increment the string upwards in alphabet starting on the right side
def IncStr(in_pass):
  global r_alphabet,s_alphabet,str_lis
#Get the current values of the string list
  for ind,let in (enumerate(reversed(in_pass))):
    str_lis[ind]=s_alphabet.index(let)
#Modify the password
  for num,inds in enumerate(str_lis):
    if(num==0):
      str_lis[num]+=1
    if(str_lis[num]==(len(s_alphabet))):
      str_lis[num]=0
      str_lis[num+1]+=1  
    in_pass=in_pass[:(len(in_pass)-num-1)]+s_alphabet[str_lis[num]]+in_pass[(len(in_pass)-num):]

  return in_pass

#Iterate over passwords
for i in xrange(1000000):
  in_pass1 = IncStr(in_pass1)
  #print in_pass1
#Test the password
  d_count=0
  t_count=0
  for i in xrange(len(r_alphabet)):
    cur_char = r_alphabet[i]
    #if((i<(len(r_alphabet)-2))):
    #  print 'Rep',r_alphabet[i:i+3],cur_char+cur_char
    if((i<(len(r_alphabet)-2)) and (r_alphabet[i:i+3] in in_pass1)):
      #print r_alphabet[i:i+3]
      t_count+=1
    if((cur_char+cur_char) in in_pass1):
      #print cur_char+cur_char 
      d_count+=1
  if(d_count>1 and t_count>0):
    print 'Pass',in_pass1
    break
  #print d_count,t_count
  #print 'O',in_pass1
