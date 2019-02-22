import uuid

class Node(object):
    id_: uuid.UUID = None
    status = None
    host: str = None
    port: str = None
    task: str = None

    def set_task(self, task: str) -> bool:
        try:
            exec(task)
            self.task = task
            return True
        except:
            return False