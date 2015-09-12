import threading


class SyCache:
    def __init__(self, lock):
        self.data = None
        self.lock = lock

    def invalidate(self):
        self.lock.acquire()
        self.data = None
        self.lock.release()

    def set(self, data):
        self.lock.acquire()
        self.data = data
        self.lock.release()


cache = SyCache(threading.Lock())
