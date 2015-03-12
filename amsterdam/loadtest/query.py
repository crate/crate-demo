from datetime import datetime

from locust import TaskSet, task, events
from locust.core import Locust
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
                request_type='execute',
                name=name or expr,
                response_time=duration,
                response_length=len(response)
            )
            return response
        except DatabaseError as e:
            events.request_failure.fire(
                request_type="execute",
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


class QueryTaskSet(TaskSet):
    """Run tasks

    Each method decorated with @task will be executed by locust.
    """

    @task
    def query(self):
        self.client.execute('SELECT * from amsterdam limit 100')

    @task
    def count(self):
        self.client.execute('SELECT count(*) from amsterdam')


class QueryLocust(CrateLocust):

    task_set = QueryTaskSet
