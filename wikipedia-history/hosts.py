import re
files = [f.strip() for f in open('files.txt').read().split() if f.strip()]

p =re.compile('enwiki-latest-pages-meta-history(\d+).xml.*')

def files_for(i):
    for name in files:
        n = int(p.match(name).group(1))
        if hash(n)%6==i:
            yield name

for i in range(6):
    host = 'st%s.p.fir.io' % (i+3)
    for f in files_for(i):
        print host, f
