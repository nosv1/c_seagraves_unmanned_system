import time

class Stopwatch:
    def __init__(self):
        self._start: float = 0
        self._end: float = 0
        self._total: float = 0

    def start(self):
        self._start = time.time()

    def stop(self):
        self._end = time.time()
        self._total = self._end - self._start