import sys,os

in_file = sys.argv[1]

ing_dict = {}
for line in open(in_file).readlines():
  l_list = line.split(' ')
  for ind,i in enumerate(l_list):
    if(i.isalpha()):
      #print i
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
        if(not metric in ing_vals[ings]):
          ing_vals[ings][metric]= {}
        ing_vals[ings][metric][tsps]=tsps*int(ing_dict[ings][metric])
# Iterate over all the numbers and find which combination gives the largest score
  for num in xrange(0,test_range):
    for num1 in xrange(0,test_range):
      for num2 in xrange(0,test_range):
        for num3 in xrange(0,test_range):
          cur_scores = {}
          cur_score = 1 
          cal_count=0
          i_count=0
          for ings,metrics in ing_vals.iteritems():
            i_count+=1
            for metric,nums in metrics.iteritems():
              if(metric=='calories'):
                if(i_count==1):
                  cal_count+=nums[num]
                if(i_count==2):
                  cal_count+=nums[num1]
                if(i_count==3):
                  cal_count+=nums[num2]
                if(i_count==4):
                  cal_count+=nums[num3]
                continue
              if(not(metric in cur_scores)):
                cur_scores[metric]=0
              if(i_count==1):
                cur_scores[metric]+=nums[num]
              if(i_count==2):
                cur_scores[metric]+=nums[num1]
              if(i_count==3):
                cur_scores[metric]+=nums[num2]
              if(i_count==4):
                cur_scores[metric]+=nums[num3]
              #print 'InScore',ings,num,num1,num2,num3,cur_scores   
          for met,score in cur_scores.iteritems():
            if(score<0):
              score=0
            cur_score*=score 
          #print 'Score',ings,num,num1,num2,num3,cur_scores,max_score,cur_score
          if((cur_score>max_score) and (num+num1+num2+num3)==100 and cal_count==500):
#          if((cur_score>max_score) and (num+num1)==100 and cal_count==500):
            #print 'Max',ings,o_ings,num,num1,cur_score  
            max_score=cur_score
  return max_score
print MaxRecipe(ing_dict,100)
