class BinOps:
  simple_add_types = ['int', 'float', 'str', 'list', 'tuple']
  add_types = {
      ('int', 'float'): 'float'
  }
  
  def add(self, parent, left, right):
    result = left.nodeType & right.nodeType & set(self.simple_add_types)
    for x in left.nodeType:
      for y in right.nodeType:
        if (x, y) in self.add_types: result.add(self.add_types[(x,y)])
        if (y, x) in self.add_types: result.add(self.add_types[(y,x)])
    parent.nodeType = parent.nodeType.union(result)
        