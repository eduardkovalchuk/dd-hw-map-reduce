import uuid
from .node import Node
from .slave import Slave
from .statuses import *


class Master(Node):

    slaves = []

    def __init__(self, host: str, port: str) -> None:
        self.id_ = uuid.uuid1()
        self.status = NEW
        self.host = host
        self.port = port

    def register_slave(self, slave: Slave) -> self:
        self.slaves.append(slave)