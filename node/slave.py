import uuid
from .node import Node
from .master import Master
from .statuses import *


class Slave(Node):
    master: Master = None

    def __init__(self, host: str, port: str, master: Master) -> None:
        self.id_ = uuid.uuid1()
        self.status = NEW
        self.host = host
        self.port = port

