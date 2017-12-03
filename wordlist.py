with open('data/mathematics_dictionary-en-sv.txt') as f:
    content = f.readlines()

content = dict([x.strip().split('=') for x in content])


def getKeysStartingWith(text):
    keys = []
    for wordArr in content:
        if (wordArr[0].startsWith(text)):
            keys += wordArr[0]
    return keys

def getTranslation(phrase):
    return content.get(phrase)
