import os

import const

x = []

def scan_dir(dir):
    ext = r".gpr.py"
    extlen = -len(ext)
                                   
    for filename in os.listdir(dir):
        name = os.path.split(filename)[1]
        if not name[extlen:] == ext:
            continue
        x.append(name)

def reg_plugins(direct):
    for (dirpath, dirnames, filenames) in os.walk(direct):
        scan_dir(dirpath)

reg_plugins(const.PLUGINS_DIR)
print x
