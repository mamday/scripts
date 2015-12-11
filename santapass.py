import sys,os

in_pass = sys.argv[1]

s_alphabet = 'abcdefghjkmnpqrstuvwxyz'

count = 0
cur_ind = -1
print in_pass
while(count<100):
  count+=1
  sa_ind = s_alphabet.index(in_pass[cur_ind])
  if((sa_ind+1)==len(s_alphabet)):
    #print sa_ind,len(s_alphabet)
    cur_ind-=1
    sa_ind=0
  in_pass = in_pass[:cur_ind]+s_alphabet[sa_ind+1] + in_pass[(len(in_pass)+cur_ind+1):]
  print in_pass
