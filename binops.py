class BinOps:
  simple_add_sub_types = ['int', 'float', 'str', 'list', 'tuple']
  add_sub_types = {
      ('int', 'float'): 'float'
  }
  simple_mult_types = ['int', 'float']
  mult_types = {
      ('int', 'float'): 'float',
      ('str', 'int'): 'str',
      ('list', 'int'): 'list'
  }
  
  def add(self, parent, left, right):
    print ('Print', left.nodeType, right.nodeType)
    result = left.nodeType & right.nodeType 
    print result
    result |= self.get_complex_types(self.add_sub_types, left, right)
    parent.nodeType |= result
  
  def sub(self, parent, left, right):
    self.add(parent, left, right)

  def mult(self, parent, left, right):
    result = left.nodeType & right.nodeType & set(self.simple_mult_types)
    result |= self.get_complex_types(self.mult_types, left, right)
    parent.nodeType |= result

  def get_complex_types(self, rules, left, right):
    result = set()
    for x in left.nodeType:
      for y in right.nodeType:
        if (x, y) in rules: result.add(rules[(x,y)])
        if (y, x) in rules: result.add(rules[(y,x)])
    return result
