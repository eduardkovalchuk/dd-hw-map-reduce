import uuid
from datetime import datetime as dt

class Task(object):

    id_: str = None
    timestamp: str = None
    content: str = None

    def __init__(self, content, id_=uuid.uuid1().hex, timestamp=dt.now().isoformat()):
        self.id_ = id_
        self.timestamp = timestamp
        self.content = content
