import basicnode
from basicnode import *

class BSTNode(Node):
  def __init__(self,val):
    Node.__init__(self,val)
    self.left = None
    self.right = None
#Add the string "Node" to the default print behavior
  def __str__(self):
    inf_str = " Node"
    out_str = super(BSTNode, self).__str__()+inf_str
    return out_str
#Insert a node into the tree (left if it is smaller than a value in the tree and right if it is larger)
  def insert(self,val):
    if self.val:
      if val < self.val:
        if self.left is None:
          self.left = BSTNode(val)
        else:
          self.left.insert(val)
      elif val > self.val:
        if self.right is None:
          self.right = BSTNode(val)
        else:
          self.right.insert(val)
    else:
      self.val=val
#Lookup the parent of a node value in the tree
  def lookup(self, val, parent=None):
    if val < self.val:
#This is what happens if the number is not in the tree
      if self.left is None:
        return None, None
#Makes self be the parent and now looking up val in the node self.left
      return self.left.lookup(val,self)
    elif val > self.val:
#This is what happens if the number is not in the tree
      if self.right is None:
        return None,None
#Makes self be the parent and now looking up val in the node self.right
      return self.right.lookup(val,self)
    else:
      return self, parent

