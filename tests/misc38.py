def win32_ver(release='',version='',csd='',ptype=''):
    if csd[:13] == 'Service Pack ':
        csd = 'SP' + csd[13:]

win32_ver()
a = 1
