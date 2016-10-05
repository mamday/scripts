import sys
import math
def answer(n):
  cur_coins = float(n)
  gauzes = 0
  while(cur_coins>0):
    cur_sqrt = math.floor(math.sqrt(cur_coins)) 
    cur_square = cur_sqrt*cur_sqrt
    print cur_square,cur_coins,gauzes 
    p_bool=True
    while(p_bool==True):
      if((cur_coins-cur_square)>=0):
        cur_coins-=cur_square
        gauzes+=1
      else:
        p_bool=False
  return gauzes

g_num = answer(sys.argv[1])
print g_num
