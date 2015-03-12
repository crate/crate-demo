# -*- coding: utf-8 -*-

from datetime import datetime

from locust import Locust, TaskSet, task, events
from locust.clients import timedelta_to_ms
from locust.exception import LocustError

from crate.client import connect
from crate.client.exceptions import DatabaseError


class CrateSession():

    def __init__(self, hosts):
        self.connection = connect(hosts)
        self.cursor = self.connection.cursor()

    def execute(self, expr, params=None, name=None):
        try:
            start = datetime.now()
            self.cursor.execute(expr, params)
            duration = timedelta_to_ms(datetime.now() - start)
            response = self.cursor.fetchall()
            events.request_success.fire(
                request_type='query',
                name=name or expr,
                response_time=duration,
                response_length=len(response)
            )
            return response
        except DatabaseError as e:
            duration = timedelta_to_ms(datetime.now() - start)
            events.request_failure.fire(
                request_type="query",
                name=name or expr,
                response_time=duration,
                exception=e,
            )


class CrateLocust(Locust):

    def __init__(self):
        super(CrateLocust, self).__init__()
        if self.host is None:
            raise LocustError("You must specify the base host. Either in the host attribute in the Locust class, or on the command line using the --host option.")
        hosts = self.host.split()
        self.client = CrateSession(hosts=hosts)


class RankingsTaskSet(TaskSet):

    @task(3)
    def get_pk(self):
        self.client.execute('''select * from rankings where "pageURL" = 'fsdpshvppquybilixlqevapin' limit 10 ''')

    @task(3)
    def count(self):
        self.client.execute('''select count(*) from rankings''');

    @task(1)
    def select(self):
        self.client.execute('''select * from rankings where "avgDuration" < 10 order by "pageRank" desc limit 10''')


class UservisitsTaskSet(TaskSet):

    @task(3)
    def destination_agg(self):
        self.client.execute('''select count(*), avg(duration) from uservisits where "destinationURL"='rggkpzvsiunisozosbmtiphydeosjsuwyzfruyundelchvtvigszqfpocyqreykowcgkquaqyjtgrpeowokcionfifgkupgyziyt' ''')

    @task(3)
    def count(self):
        self.client.execute('''select count(*) from uservisits''')

    @task(1)
    def select_ordered(self):
        self.client.execute('''select * from uservisits where "cCode" = 'AUT' and "adRevenue" < 0.1 order by "adRevenue" desc limit 10''')

    @task(1)
    def select_fultext(self):
        self.client.execute('''select "UserAgent", _score from uservisits where match("UserAgent", 'vista windows') order by 2 desc limit 10 ''')

class SystemTaskSet(TaskSet):

    @task(1)
    def s1(self):
        self.client.execute('''select count(*) from sys.shards''')

    @task(1)
    def s2(self):
        self.client.execute('''select table_name, state, "primary", count(*)  from sys.shards group by 1,2,3 order by 1 limit 100 ''')

class CrateTaskSet(TaskSet):

    tasks = {
        UservisitsTaskSet: 5,
        RankingsTaskSet: 5,
        SystemTaskSet: 1,
        }


class QueryLocust(CrateLocust):

    task_set = CrateTaskSet
