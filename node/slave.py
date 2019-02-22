import uuid
from .master import Master

class Slave(object):
    id_: uuid.UUID = None
    host = ""
    port = ""
    master: Master = None

    def __init__(self, host: str, port: str, master: Master) -> None:
        self.id_ = uuid.uuid1()
        self.host = host
        self.port = port

