import sys
import time
import random

from crate.client import connect
from threading import Thread
from Queue import Queue
from uuid import uuid1

host = sys.argv[1]

concurrency = 20

connection = connect(host)

cursor = connection.cursor()
q = Queue()


try:
    #cursor.execute('DROP TABLE amsterdam')
    a = true
except Exception:
    pass
try:
    cursor.execute('''
        CREATE TABLE amsterdam (
            id string primary key,
            count integer,
            info string,
            ts timestamp
        ) clustered into 120 shards
          with (number_of_replicas = 0)
    ''')

except Exception:
    pass

cursor.execute('''
    ALTER TABLE amsterdam SET (refresh_interval = -1)
''')

STEP = 1000

if len(sys.argv) > 2:
    NUM_ENTRIES = int(sys.argv[2])
else:
    NUM_ENTRIES = 1000000

now = int(time.time() * 1000)
day = 60 * 60 * 24 * 1000

print 'creating', NUM_ENTRIES, 'entries in blocks of', STEP
ins = "INSERT INTO amsterdam (id, count, info, ts) VALUES " + ', '.join(["(?, ?, ?, ?)"] * STEP)


def worker(cursor):
    while True:
        params = q.get()
        cursor.execute(ins, params)
        q.task_done()


def launch_workers():
    for i in xrange(concurrency):
        c = connection.cursor()
        t = Thread(target=worker, args=(c,))
        t.daemon = True
        t.start()

launch_workers()
for i in xrange(1, NUM_ENTRIES, STEP):
    params = []
    for a in xrange(i, i + STEP):
        params.extend(['id' + uuid1().hex, a, 'info' + str(i), now - random.randint(0, day * 100)])
    q.put(params)


q.join()
cursor.execute('''
    ALTER TABLE amsterdam SET (refresh_interval = 1000)
''')
