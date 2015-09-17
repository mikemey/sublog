import threading


class SyCache:
    def __init__(self, default=None, lock=threading.Lock()):
        self.data = default
        self.default = default
        self.lock = lock

    def invalidate(self):
        self.lock.acquire()
        self.data = self.default
        self.lock.release()

    def set(self, data):
        self.lock.acquire()
        self.data = data
        self.lock.release()

    def get(self):
        self.lock.acquire()
        data = self.data
        self.lock.release()
        return data
