class HitsCounter(object):
    def __init__(self, verbose = False):
        self.total   = 0
        self.hits    = 0
        self.misses  = 0
        self.verbose = verbose

    def check_condition(self, cond, msg):
        self.total += 1
        if cond:
            self.hits   += 1
        else:
            if self.verbose:
                print 'Miss: %s' % msg
            self.misses += 1

    def __str__(self):
        return 'Total: %d, hits: %d, misses: %d' % (self.total, self.hits, self.misses)
