import pickle
import uuid
import functools as ft
import requests
import os
from typing import List, Tuple, Hashable, Any, Iterable
from multiprocessing.dummy import Pool
import multiprocessing as mp

from node.statuses import *
from node.actions import *
from node.task import Task
from node.node import Node


class Master(Node):

    def __init__(self, host: str, port: int, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port
        self.task = None
        self.slaves: List['Slave'] = []

    def register_slave(self, id_: str, host: str, port: str, status: str) -> 'Slave':
        obj = Slave(host, port, id_=id_, status=status)
        self.slaves.append(obj)
        return obj

    def send_task(self) -> Task:
        data = self.task.__repr__()
        for slave in self.slaves:
            set_task_url = slave.url + SET_TASK
            req = requests.post(set_task_url, json=data)
            if req.status_code != 201:
                self.status = FAIL
                raise Exception('UNABLE TO SET TASK AT: {}'.format(slave.url))

    def trigger_map(self, slave) -> List:
        run_map_url = slave.url + RUN_MAP
        req = requests.get(run_map_url)
        if req.status_code == 200:
            data = req.json()
            result = data['map_result']
            return result
        else:
            self.status = FAIL
            raise Exception(req.json())
    
    def run_map_on_cluster(self) -> List:
        pool = Pool(mp.cpu_count()*3)
        map_result = pool.map(self.trigger_map, self.slaves)
        return map_result

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
    
    def sync_cluster_data(self):
        updated = []
        for slave in self.slaves:
            fail_connection_msg = 'LOST CONNECTION TO SLAVE AT: {}'.format(slave.url)
            try:
                req = requests.get(slave.url)
                if req.status_code == 200:
                    data = req.json()
                    slave.load_from_dict(data)
                    updated.append(slave)
                else:
                    print(fail_connection_msg)
            except:
                print(fail_connection_msg)
        self.slaves = updated
        return self

    
    def submit(self, task: str):
        self.set_task(task)
        self.sync_cluster_data()
        self.send_task()
        return self
    
    def flatten(self, map_result: Iterable[Iterable]) -> Iterable:
        return ft.reduce(lambda x,y: x + y, map_result)

    def group_by_key(self, to_group: Iterable) -> Iterable:
        flat = self.flatten(to_group)
        
        keys = dict(flat).keys()
        result = dict([(k, []) for k in keys])

        for k, v in flat:
            result[k].append(v)

        return result.items()

    def do_reduce(self, grouped_by_key: Iterable) -> Iterable:
        if self.task is None:
            raise Exception("Task is not set")
        
        keys, values = self.unzip(grouped_by_key)
        result = map(self.task.reduce_cls.reduce, keys, values)
        return dict(result)

class Slave(Node):

    def __init__(self, host: str, port: int, id_ = uuid.uuid1().hex, status = NEW) -> None:
        self.id_ = id_
        self.status = status
        self.host = host
        self.port = port
        self.task = None
        self.master: Master = None

    def load_from_dict(self, data):
        self.id_ = data['id_']
        self.status = data['status']
        self.host = data['host']
        self.port = data['port']
        if data['task']:
            task = Task(data['task']['content'],data['task']['id_'], data['task']['timestamp'])
            self.task = task

    def register_master(self, host: str, port: int) -> None:
        reg_url = 'http://{}:{}{}'.format(host, port, REGISTER_SLAVE)
        req = requests.post(reg_url, json=self.__repr__())
        if req.status_code != 201:
            raise Exception('Unable to register at MASTER')
        master_data = req.json()
        master = Master(host, port, master_data['id_'], master_data['status'])
        self.master = master
        return master

    def load_data(self, path: str) -> List[Tuple[Hashable, Any]]:
        with open(path, 'rb') as to_load:
            loaded = pickle.load(to_load)
        return loaded

    def save_data(self, path: str, data: Iterable) -> 'Slave':
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'wb') as to_save:
            pickle.dump(data, to_save, pickle.HIGHEST_PROTOCOL)
        return self

    def do_map(self, path):
        if self.task is None:
            raise Exception("Task is not set")
        
        data = self.load_data(path)
        keys, values = self.unzip(data)

        result = map(self.task.map_cls.map, keys, values)
        return [list(el) for el in result]
