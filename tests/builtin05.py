import os
import const
for (x, y, z) in os.walk(const.DIR_FOR_BUILTIN05):
    print x, y, z
