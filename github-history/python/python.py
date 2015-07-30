#!/usr/bin/python

from crate import client

connection = client.connect("http://192.168.59.103:4200")

cursor.execute("SELECT * FROM ghevent limit 100")
result = cursor.fetchall()
print result
cursor.close()
connection.close()
