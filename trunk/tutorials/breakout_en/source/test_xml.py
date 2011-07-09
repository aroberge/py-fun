from xml.etree import ElementTree

with open('index.xml', 'r') as f:
    tree = ElementTree.parse(f)

a = tree.find('hidden_code')
c = tree.find('c')
print c

def tag_content(elem):
    tag = elem.tag
    tag_length = len(elem.tag)+2
    return ElementTree.tostring(a, encoding="utf-8")[tag_length: -(tag_length+2)]

print tag_content(a)