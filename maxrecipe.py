import sys,os

in_file = sys.argv[1]

ing_dict = {}
for line in open(in_file).readlines():
  l_list = line.split(' ')
  for ind,i in enumerate(l_list):
    if(i.isalpha()):
      print i
      if(not(l_list[0] in ing_dict)):
        ing_dict[l_list[0]]={}
      ing_dict[l_list[0]][i]= l_list[ind+1][:-1]

print ing_dict

def MaxRecipe(cookie_dict,test_range=1000):
  max_score=0  
  ing_vals = {}
#Get total scores for different numbers of ingredients (up to 1000 by default)
  for ings,vals in ing_dict.iteritems():
    for tsps in xrange(0,test_range):
      for metric in ing_dict[ings]:
        if(not ings in ing_vals):
          ing_vals[ings]={}
        if(not tsps in ing_vals[ings]):
          ing_vals[ings][tsps]= {}
        ing_vals[ings][tsps][metric]=tsps*int(ing_dict[ings][metric])
# Iterate over all the numbers and find which combination gives the largest score
  for ings,nums in ing_vals.iteritems():
    for o_ings,o_nums in ing_vals.iteritems():
       if(o_ings!=ings): 
         for num,metrics in nums.iteritems():
           for num1,metrics1 in o_nums.iteritems():
             cur_scores = {}
             cur_score = 1 
             for metric,vals in metrics.iteritems():
               if(metric=='calories'):
                 continue
               if(not(metric in cur_scores)):
                 cur_scores[metric]=0
               cur_scores[metric]+=vals
               cur_scores[metric]+=metrics1[metric]
             #print num,num1,cur_scores   
             for met,score in cur_scores.iteritems():
               if(score<0):
                 score=0
               cur_score*=score 
             print 'Score',ings,o_ings,num,num1,cur_scores,cur_score
             if((cur_score>max_score) and (num+num1)==100):
               #print 'Max',ings,o_ings,num,num1,cur_score  
               max_score=cur_score
  return max_score
print MaxRecipe(ing_dict,3)
