with open('data/mathematics_dictionary-en-sv.txt') as f:
    content = f.readlines()

content = dict([x.strip().split('=') for x in content])


def getKeysStartingWith(text):
    keys = []
    for key in content:
        if (key.startswith(text)):
            keys.append(key)
    return keys

def getTranslation(phrase):
    tr = content.get(phrase)
    if tr != None:
        return tr.lower()
    else:
        return None
