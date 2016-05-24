class Node(object):
  def __init__(self,val):
    self.val = val
  def __str__(self):
    return self.val
  def getCurVal(self):
    return self.val 
  def setCurVal(self,val):
    self.val=val
