#Treat grid like a binary tree. Traverse tree starting in the direction that is most food expensive to try to greedily optimize the time it takes to get the correct answer. 
def answer(food, grid):
  min_food = 99 
  food_list = [food]
  node_list = [(0,0)]
  num_cols = len(grid)
  num_rows = len(grid[0])
  num_nodes = num_rows*num_cols 
  res_dict = {}
#Iterate through all the nodes until either we have traversed the entire grid/tree or the maximum food value is used (result is 0)
  while(len(node_list)>0 and min_food>0):
    cur_food = food_list.pop()
    cur_node = node_list.pop()
    #print cur_food,cur_node,min_food,node_list,food_list
#Get the current food value and subtract it from cur_food
    cur_val = grid[cur_node[0]][cur_node[1]]
    cur_food-=cur_val
#Determine the indices of the down and rightward nodes
    down_ind = cur_node[0]+1
    right_ind = cur_node[1]+1
    right_node = None
    down_node = None
#Get the right and down nodes if they exist
    if(right_ind<num_rows):
      right_node = (cur_node[0],right_ind)
    if(down_ind<num_cols):
      down_node = (down_ind,cur_node[1])
#If there is no down and no right node we are at the end. Save the minimum amount of food if it is lower than the previous minimum (as long as it is a positive amount of food).
    if(right_node==None and down_node==None):
      if(cur_food>=0 and cur_food<min_food):
        min_food=cur_food
      continue
#Get the right and down food values if they exist
    right_val = -1
    down_val = -1
    if(right_node!=None):
      right_val = grid[right_node[0]][right_node[1]]
    if(down_node!=None):
      down_val = grid[down_node[0]][down_node[1]]
#Append the nodes to the list so that the larger value gets popped first.
    if(right_val>down_val):
      if(down_val!=-1):
        node_list.append(down_node)    
        food_list.append(cur_food)
      node_list.append(right_node)
      food_list.append(cur_food)
    else:
      if(right_val!=-1):
        node_list.append(right_node)    
        food_list.append(cur_food)
      node_list.append(down_node)
      food_list.append(cur_food)
  if(min_food==99):
    min_food=-1
  return min_food


'''Treat grid like a binary tree. Traverse tree starting in the direction
that is most food expensive to try to greedily optimize the time it takes
to get the correct answer.''' 
def ganswer(food, grid):
    food_list = [food]
    node_list = [(0,0)]
    past_nodes = []
    past_food = []
    num_cols = len(grid)
    num_rows = len(grid[0])
    num_nodes = num_rows*num_cols
    res_dict = {} 
    '''Iterate through all the nodes until either we have traversed 
    the entire grid/tree or the maximum food value is used (result is 0)'''
    while(len(node_list)>0):
        cur_food = food_list.pop()
        cur_node = node_list.pop()
        cur_val = grid[cur_node[0]][cur_node[1]]
        #Determine the indices of the down and rightward nodes
        down_ind = cur_node[0]+1
        right_ind = cur_node[1]+1
        right_node = None
        down_node = None
        #Get the right and down nodes if they exist
        if(right_ind<num_rows):
            right_node = (cur_node[0],right_ind)
        if(down_ind<num_cols):
            down_node = (down_ind,cur_node[1])
        '''If there is no down and no right node we are at the end.
        Save the minimum amount of food if it is lower than the
        previous minimum (as long as it is a positive amount of food).'''
        if((right_node==None and down_node==None) or (cur_node in res_dict)):
            r_node=False
            '''Keep track of how much food was used between a node and the end.
            Save the results as a set in a dictionary indexed by node.'''
            prev_node = cur_node
            if(not(cur_node in res_dict)):
              res_dict[cur_node]=set([cur_val])
            while(r_node==False and len(past_food)>0):
              h_node = past_nodes.pop()
              h_food = past_food.pop()
              for f_val in res_dict[prev_node]:
                if(not(h_node in res_dict)):
                  res_dict[h_node]=set([f_val+h_food])
                else:
                  res_dict[h_node].add(f_val+h_food)
              prev_node = h_node
              '''Stop iterating through nodes when we hit a fork.'''
              if(len(past_nodes)>0 and h_node==past_nodes[-1]):
                r_node=True 
            '''Once the while loop is finished then continue to next node'''
            continue
        #Get the right and down food values if they exist
        right_val = -1
        down_val = -1
        #Get the current food value and subtract it from cur_food
        cur_food-=cur_val
        if(right_node!=None):
            right_val = grid[right_node[0]][right_node[1]]
        if(down_node!=None):
            down_val = grid[down_node[0]][down_node[1]]
        #Append the nodes to the list so that the larger value gets popped first.
        if(right_val>down_val):
            if(down_val!=-1):
                node_list.append(down_node)
                food_list.append(cur_food)
        	past_nodes.append(cur_node)
        	past_food.append(cur_val)
            node_list.append(right_node)
            food_list.append(cur_food)
            past_nodes.append(cur_node)
            past_food.append(cur_val)
        else:
            if(right_val!=-1):
                node_list.append(right_node)
                food_list.append(cur_food)
                past_nodes.append(cur_node)
                past_food.append(cur_val)
            node_list.append(down_node)
            food_list.append(cur_food)
            past_nodes.append(cur_node)
            past_food.append(cur_val)
    '''Find the minimum necessary food to feed the zombie'''
    min_food=99
    for i in res_dict[(0,0)]:
      if((food-i)>=0 and (food-i)<min_food):
        min_food=(food-i)
    if(min_food==99):
      min_food=-1
    return min_food

#ta = ganswer(3,[[0, 2, 5], [1, 1, 3], [2, 1, 1]])
#ta = ganswer(7,[[0, 2, 5], [1, 1, 3], [2, 1, 1],[4,4,1]])
ta = ganswer(7,[[0, 2, 5,1], [1, 1, 3,1], [2, 1, 1,1]])
'''ta = ganswer(197,[[0, 2, 5,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[1, 1, 3,1], 
[2, 1, 1,1]])
'''
print ta
