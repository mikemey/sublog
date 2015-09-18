import threading


class SyCache:
    def __init__(self, default=None):
        self.data = {}
        self.default = default

    def invalidate(self, key):
        self.ensure_entry(key)
        self.data[key].set(self.default)

    def set(self, key, value):
        self.ensure_entry(key)
        self.data[key].set(value)

    def get(self, key):
        self.ensure_entry(key)
        return self.data[key].get()

    def ensure_entry(self, key):
        if key not in self.data:
            self.data[key] = CacheEntry(self.default)


class CacheEntry:
    def __init__(self, value, lock=threading.Lock()):
        self.lock = lock
        self.value = value

    def get(self):
        self.lock.acquire()
        val = self.value
        self.lock.release()
        return val

    def set(self, value):
        self.lock.acquire()
        self.value = value
        self.lock.release()
