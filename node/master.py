import uuid
from .slave import Slave


class Master(object):
    id_: uuid.UUID = None
    host = ""
    port = ""
    slaves = []

    def __init__(self, host: str, port: str) -> None:
        self.id_ = uuid.uuid1()
        self.host = host
        self.port = port

    def register_slave(self, slave: Slave) -> self:
        self.slaves.append(slave)

    # def submit_task()