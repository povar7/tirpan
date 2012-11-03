import os
for (dirpath, dirnames, filenames) in os.walk('tests/import03'):
    print dirpath, dirnames, filenames
