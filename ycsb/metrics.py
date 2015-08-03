from crate import client
import sys
import csv
import sched, time

def run(connection, file_name):
  cursor = queryNodes(connection)
  data = cursor.fetchall()
  wr = csv.writer(open(file_name, 'a'), delimiter=',')
  for record in data:
    wr.writerow(record)

def queryNodes(connection):
  cursor = connection.cursor()
  cursor.execute("""select mem['probe_timestamp'] as timestamp, hostname,
        load['1'] as load_1, load['5'] as load_5, load['15'] as load_15,
        mem['free_percent'] as mem_free_persent, mem['used_percent'] as mem_used_percent, mem['free'] as mem_free,
        heap['used'] as heap_used, heap['free'] as heap_free, heap['max'] as heap_max,
        network['tcp']['packets']['sent'] as packets_sent, network['tcp']['packets']['received'] as packets_received,
        fs['total']['reads'] as fs_reads, fs['total']['writes'] as fs_writes from sys.nodes""")
  return cursor

if __name__ == "__main__":

  hosts = sys.argv[2:]
  file_name = sys.argv[1]
  print 'Hosts list', hosts

  connection = client.connect(hosts)

  # first call to get a schema
  cursor = queryNodes(connection)
  schema = [attr[0] for attr in cursor.description]

  print schema
  wr = csv.writer(open(file_name, 'w'), delimiter=',')
  wr.writerow(schema)
  while True:
    time.sleep(5)
    run(connection, file_name)





