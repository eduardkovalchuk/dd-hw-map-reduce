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
    from node.statuses import *
    from node.actions import *
    from node.task import Task

class Node(object):
    id_: str = None
    status: str = None
    host: str = None
    port: int = None
    task: Task = None
    
    def __repr__(self) -> dict:
        dic = self.__dict__
        dic['task'] = self.task.__repr__()
        return dic

    def __str__(self) -> str:
        return self.__repr__().__str__()

    def check(self) -> 'Node':
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

    def register_slave(self, slave_id: str, slave_host: str, slave_port: str) -> 'Slave':
        obj = Slave(slave_host, slave_port, self, slave_id, ACTIVE)
        self.slaves.append(obj)
        return obj

    def send_task(self) -> Task:
        data = self.task.__dict__
        for slave in self.slaves:
            set_task_url = slave.url + SET_TASK
            req = requests.post(set_task_url, data)
            if req.status_code == 201:
                return self.task
            else:
                self.status = FAIL
                raise Exception(req.json())

    def trigger_task(self) -> Task:
        for slave in self.slaves:
            run_task_url = slave.url + RUN_TASK
            req = requests.get(run_task_url)
            if req.status_code == 200:
                return self.task
            else:
                self.status = FAIL
                raise Exception(req.json())

    def check_cluster_task(self) -> bool:
        res = True
        for slave in self.slaves:
            heartbeat_url = slave.url
            req = requests.get(heartbeat_url)
            if req.status_code == 200:
                slave_data = req.json()
                valid_task = self.task.id_ == slave_data['task']['id_']
                res = res and valid_task
            else:
                raise Exception(req.json())
        return res
                



class Slave(Node):

    master: Master = None

    def __init__(self, host: str, port: int, master: Master, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port


task = Task("some content")


# node = Node()
# node.id_ = uuid.uuid1().hex
# node.host = 'localhost'
# node.port = 1234
# node.task = task

# print(node.__repr__())
# print(task.__repr__())


# master = Master("localhost", 1234)
# dic = master.__dict__
