import gettext as pgettext

def gettext(msgid):
    if len(msgid.strip()) == 0:
        return msgid
    return unicode(pgettext.gettext(msgid))
