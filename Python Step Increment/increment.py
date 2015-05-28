#!/usr/bin/python

from crate import client
import time
from random import randint


connection = client.connect("http://st01p.aws.fir.io:4200")

tmptime = int(time.time())
print tmptime

rndsteps = randint(1,30)
print rndsteps

cursor = connection.cursor()

cursor.execute("INSERT INTO steps (num_steps, ts, username) VALUES (?, ?, ?)", (tmptime, rndsteps, 'gosinski'))

print ("Steps Incremented")
# insert into steps (month_partition, num_steps, payload, ts, username) VALUES ();

cursor.execute("SELECT * FROM steps WHERE username = ? AND ts = ?", ('gosinski', tmptime))
cursor.arraysize = 1000
result = cursor.fetchmany()
print(result)

cursor.close()
connection.close()
