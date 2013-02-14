class DefectCollector(object):
  def __init__(self):
    self.defects = []

  def add_defect(self,name, node):
    print "\t\t", name
    self.defects.append((name, node))