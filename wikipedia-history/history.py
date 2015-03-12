import xml.parsers.expat, sys
import logging
import time
import os
import json
from datetime import datetime
import calendar

def to_ts(datestr):
    try:
        dt = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ')
        ts = calendar.timegm(dt.utctimetuple())
        return int(ts * 1000)
    except ValueError:
        return 0

class Parser(object):

    # prepare for parsing

    def __init__(self, limit=0):
        self.f_out = os.fdopen(sys.stdout.fileno(), 'wb', 256*1024)
        self.f_in = os.fdopen(sys.stdin.fileno(), 'rb', 16*1024)
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.CharacterDataHandler = self.handleCharData
        self.parser.StartElementHandler = self.handleStartElement
        self.parser.EndElementHandler = self.handleEndElement
        self.limit = limit

    def parse(self):
        self.t = self.start_time = time.time()
        self.pos = 0
        self.path = []
        self.parser.ParseFile(self.f_in)
        self.context = None

    def handleCharData(self, data):
        if len(self.path)<3:
            return
        context, attr = self.path[-2:]
        if context == 'revision':
            if attr == 'id':
                assert not hasattr(self.rev, '_id')
                #if int(data)==0:
                #    print >>sys.stderr,self.page_id, self.path, data, self.rev
                self.rev['_id'] = data
                self.rev['rev_id'] = int(data)
            elif attr == 'parentid':
                self.rev['parent_id'] = int(data)
            elif attr == 'comment':
                if self.rev.has_key(attr):
                    self.rev[attr] += data
                else:
                    self.rev[attr] = data
            elif attr == 'timestamp':
                self.rev['ts'] = to_ts(data)
        elif context == 'contributor':
            o = self.rev['contributor']
            if attr == 'id':
                o['id'] = int(data)
            elif attr == 'username':
                o['username'] = data
            elif attr == 'ip':
                o['ip'] = data
        elif context == u'page':
            atrr = self.path[-1]
            if attr == u'id':
                self.page_id = int(data)
            elif attr == 'title':
                self.page_title = data
            elif attr == 'ns':
                self.page_ns = int(data)

    def handleStartElement(self, name, attrs):
        self.path.append(name)
        if name == 'revision':
            self.pos += 1
            self.rev = dict(page_id=self.page_id,
                            title=self.page_title,
                            ns=self.page_ns)
            if self.limit and self.pos>self.limit:
                raise StopIteration
        elif name == 'contributor':
            self.rev['contributor'] = {}
        elif name == 'minor':
            self.rev['minor'] = True

    def output(self, o):
        self.f_out.write(json.dumps(o, separators=(',',':')))
        self.f_out.write('\n')

    def handleEndElement(self, name):
        if name=='revision':
            if self.pos%10000==0:
                td = time.time()-self.t
                self.t = time.time()
                logging.info("docs: %s, %s, %02d",
                             self.pos, int(self.t - self.start_time) ,10000/td)
            self.output(self.rev)
            self.rev=None

        assert name == self.path.pop()

def main():
    logging.basicConfig(level=logging.INFO)
    p = Parser()
    p.parse()

if __name__ == '__main__':
    main()
