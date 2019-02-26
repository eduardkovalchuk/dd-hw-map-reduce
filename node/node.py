import uuid
import requests
import json
import pickle
from typing import List, Tuple, Hashable, Any, Iterable
from datetime import datetime as dt

from node.statuses import *
from node.actions import *
from node.task import Task

class Node(object):
    id_: str = None
    status: str = None
    host: str = None
    port: int = None
    task: Task = None

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)

    def __str__(self) -> str:
        return self.__repr__().__str__()
    
    def __repr__(self):
        if self.task:
            task = self.task.__repr__()
        else:
            task = None
        return {
            'id_' : self.id_,
            'status': self.status,
            'host': self.host,
            'port': self.port,
            'task': task
        }

    def check(self) -> 'Node':
        return self

    def set_task(self, task: str, id_: str=uuid.uuid1().hex, timestamp: str=dt.now().isoformat()) -> bool:
        try:
            obj = Task(task, id_=id_, timestamp=timestamp)
            self.task = obj
            return True
        except:
            return False

    # def map(self, key, value):
    #     exec(self.task.content)
    #     return Map.map(key, value)


# task = Task("some content")
# node = Node()
# node.id_ = uuid.uuid1().hex
# node.host = 'localhost'
# node.port = 1234
# node.task = task

# print(node.__repr__())
# print(task.__repr__())

