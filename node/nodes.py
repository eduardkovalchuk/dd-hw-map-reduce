import uuid
import requests
import json

if __name__ == "__main__":
    from statuses import *
else:
    from node.statuses import *


class Node(object):
    id_: str = None
    status = None
    host: str = None
    port: int = None
    task: str = None

    def check(self):
        return self

    def set_task(self, task: str) -> bool:
        try:
            exec(task)
            self.task = task
            return True
        except:
            return False


class Master(Node):

    slaves = []

    def __init__(self, host: str, port: int, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port

    def register_slave(self, slave_id: str, slave_host: str, slave_status: str, slave_port: str) -> None:
        # self.slaves.append(slave)
        slave = Slave(slave_host, slave_port, self, slave_id, slave_status)
        self.slaves.append(slave)
    
    def send_task(self):
        # for slave in self.slaves:
        #     requests.post()
        pass


class Slave(Node):
    master: Master = None

    def __init__(self, host: str, port: int, master: Master, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port
