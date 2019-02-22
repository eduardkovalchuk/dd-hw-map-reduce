import uuid
import requests
import json
from typing import List
from datetime import datetime as dt

if __name__ == '__main__':
    from statuses import *
    from actions import *
    from task import Task
else:
    print("="*100)
    from node.statuses import *
    from node.actions import *
    from node.task import *


class Node(object):
    id_: str = None
    status: str = None
    host: str = None
    port: int = None
    task: Task = None
    
    def __str__(self):
        return self.__dict__.__str__()

    def check(self):
        return self

    def set_task(self, task: str) -> bool:
        try:
            exec(task)
            self.task = task
            return True
        except:
            return False

    @property
    def url(self):
        return 'http://{}:{}/'.format(self.host, self.port)



class Master(Node):

    slaves: List['Slave'] = []

    def __init__(self, host: str, port: int, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port

    def register_slave(self, slave_id: str, slave_host: str, slave_status: str, slave_port: str) -> 'Slave':
        obj = Slave(slave_host, slave_port, self, slave_id, slave_status)
        self.slaves.append(obj)
        return obj

    def send_task(self):
        data = self.task.__dict__
        for slave in self.slaves:
            set_task_url = slave.url + SET_TASK
            requests.post(set_task_url, data)
        return self

    def trigger_task(self):
        pass


class Slave(Node):

    master: Master = None

    def __init__(self, host: str, port: int, master: Master, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port


# node = Node()
# node.host = 'localhost'
# node.port = 1234

# print(node.url)


# master = Master("localhost", 1234)
# dic = master.__dict__
