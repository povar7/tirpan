class Date(object):
    CAL_GREGORIAN = 0

    def __init__(self, *source):
        if isinstance(source, tuple):
            self.calendar = Date.CAL_GREGORIAN
        elif source:
            self.calendar = source.calendar
        else:
            self.calendar = Date.CAL_GREGORIAN

date1 = Date(0)
date2 = Date()
