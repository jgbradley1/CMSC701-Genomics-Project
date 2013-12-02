'''
Test out file writing:
'''


refs = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
queries = ['aa', 'dd', 'aaa', 'eee', 'gg', 'bbb', 'cc', 'ccc']


dir = "testfiles/"
filemap = {}

for ref in refs:
    filemap[ref] = open(dir + ref, 'r+')
    filemap[ref].write(ref)

for ref in refs:
    for query in queries:
        if ref[0] == query[0]:
            filemap[ref].write('\t' + query)

for ref in refs:
    filemap[ref].close()

final = open(dir + "final", 'w')
for ref in refs:
    with open(dir + ref, 'r+') as f:
        for line in f:
            final.write(line + '\n')

