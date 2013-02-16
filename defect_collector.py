class DefectCollector(object):
  def __init__(self):
    self.defects = []

  def add_defect(self, defect):
    print "\t\t", defect
    self.defects.append(defect)
