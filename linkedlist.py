import basicnode
from basicnode import Node 

#My list node implementation
class LLNode(Node):
  def __init__(self,val,ind):
    Node.__init__(self,val)
    self.ind = ind 
    self.next = None 
  def getCurInd(self):
    return self.ind 
  def getNext(self):
    return self.next
  def setNext(self,newnext):
    self.next=newnext

#My linked list implementation
class MyList(object):
  def __init__(self):
#Initialize the node to None and the index to zero
    self.cur_node=None
    self.cur_ind=0
  def isEmpty(self):
#Determine if the list is empty
    return self.cur_node == None
  def __str__(self):
#This prints the list reversed bracketed by [M M]
    if(self.isEmpty()):
      return "No Entries"
    full_lis = "[M "
    node = self.cur_node
    count = 0
    while node != None:
      count = count + 1
      full_lis+=' '+str(node.getCurVal())+' '
      node = node.getNext()
    full_lis+= " M]"
    return full_lis
  def addVal(self,val):
#Add a node to the list with value val at the currently available index position
    new_node = LLNode(val,self.cur_ind)
    new_node.setNext(self.cur_node)  
    self.cur_node = new_node
    self.cur_ind+=1
  def getSize(self):
#Get the current size of the list
    node = self.cur_node
    count = 0
    while node != None:
      count = count + 1
      node = node.getNext()
    return count
  def getInd(self,val):
#Get the index of the first node with value val
    node = self.cur_node
    if(node==None):
      return "List is empty"
    while node != None:
      if(node.getCurVal()==val):
        return node.getCurInd()
      node = node.getNext()
    return "Did not find entry"
  def getVal(self,ind):
#Get the value of the node at index ind
    node = self.cur_node
    while node != None:
      if(node.getCurInd()==ind):
        return node.getCurVal()
      node = node.getNext()
    return "Index is out of range"
  def delVal(self,val):
    node = self.cur_node
    prev_node = None
    del_bool = False
    if(node==None):
      return "List is empty"
#Delete Node with value val
    while node != None:
      if(not(del_bool)):
        node.ind-=1
        if(node.getCurVal()==val):
          del_bool = True 
          if(prev_node):
            prev_node.setNext(node.getNext())
          else:
            self.cur_node=node.getNext() 
          break
      prev_node=node
      node = node.getNext()
    if(not(del_bool)):
      return "Did not find entry"
  def delInd(self,ind):
    node = self.cur_node
    prev_node = None
    del_bool = False
    if(node==None):
      return "List is empty"
    elif(ind<0 or ind>(self.getSize()-1)):
      return "Index is out of range"
#Delete Val at index ind after decreasing the index of the previous nodes
    while node != None:
      if(not(del_bool)):
        node.ind-=1
        if(node.getCurInd()==ind):
          del_bool = True 
          if(prev_node):
            prev_node.setNext(node.getNext())
          else:
            self.cur_node=node.getNext() 
          break
      prev_node=node
      node = node.getNext()
  def insertValue(self,val,ind):
    node = self.cur_node
    new_node = LLNode(val,ind)
    prev_node = None
    ins_bool = False
    if(ind<0 or ind>(self.getSize())):
      return "Index is out of range"
#Insert value val and index ind, and increase indices of previous nodes
    while node != None:
      if(not(ins_bool)):
        node.ind+=1
        if(node.getCurInd()==ind):
          ins_bool = True 
          node.ind-=1
          if(prev_node):
            prev_node.setNext(new_node)
            new_node.setNext(node)
          else:
            new_node.setNext(self.cur_node)
            self.cur_node=new_node
            self.cur_ind+=1
          break
        if(ind==0 and node.getCurInd()==1):
          node.setNext(new_node)
          new_node.setNext(None)
          break
      prev_node=node
      node = node.getNext()
       
