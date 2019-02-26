import uuid
from copy import copy
from datetime import datetime as dt

class Task(object):

    id_: str = None
    timestamp: str = None
    content: str = None

    def __init__(self, content, id_=uuid.uuid1().hex, timestamp=dt.now().isoformat()):
        self.id_ = id_
        self.timestamp = timestamp
        self.content = content

        # extract Map and Reduce classes
        exec(content)
        self.map_cls = locals()['Map']
        self.reduce_cls = locals()['Reduce']

    def __repr__(self):
        dic = copy(self.__dict__)
        dic.pop('map_cls')
        dic.pop('reduce_cls')
        return dic