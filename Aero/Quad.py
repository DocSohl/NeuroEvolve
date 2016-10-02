import threading
from collections import namedtuple
import pygame

Params = namedtuple("Params", "x y z rx ry rz")

def runQuad(q):
    q.run()

class Quad:
    def __init__(self):
        self._lock = threading.Lock()
        self._params = Params(0,0,0,0,0,0)
        self._running = True
        self._clock = pygame.time.Clock()

    def get_params(self):
        with self._lock:
            return self._params

    def set_params(self, x, y, z, rx, ry, rz):
        with self._lock:
            self._params = Params(x,y,z,rx,ry,rz)

    def run(self):
        while self._running:
            p = self._params
            self.set_params(p.x, p.y, p.z, p.rx+0, p.ry+1, p.rz+0)
            self._clock.tick(50)

    def quit(self):
        self._running = False