#!/usr/bin/python

from crate import client
import time
from datetime import datetime
from random import randint


connection = client.connect("http://st01p.aws.fir.io:4200")

tmptime = int(time.time())
print tmptime

rndsteps = randint(1,30)
print rndsteps

# TODO: Dynamic
currentmonth = datetime.now().year + datetime.now().month
print currentmonth

cursor = connection.cursor()

returnTrue = cursor.executemany("INSERT INTO steps (num_steps, ts, username, month_partition) VALUES (?, ?, ?, ?)", [(rndsteps, tmptime, 'gosinski', currentmonth)])

print returnTrue
print ("Steps Incremented")

# TODO: This takes a long time
cursor.execute("SELECT * FROM steps WHERE username = ? AND ts = ?", ('gosinski', tmptime))
result = cursor.fetchall()

while len(result) == 0:
    print "Not updated"
    time.sleep(5)
    cursor.execute("SELECT * FROM steps WHERE username = ? AND ts = ?", ('gosinski', tmptime))
    result = cursor.fetchall()

print "Updated"
cursor.close()
connection.close()
