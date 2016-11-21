import threading
from collections import namedtuple
import pygame
import numpy as np
import quaternion

Props = namedtuple("Props", "a b c d")


# Propeller configuration
# A     B    ^ z
#  \   /     |
#   |-|      y--> x
#  /   \
# D     C
# Clockwise: A, C
# Counter: B, C

def runQuad(q):
    q.run()


class Quad:
    def __init__(self):
        self._lock = threading.Lock()
        self._position = np.array([0, 0, 0], dtype='float32').T
        self._orientation = np.quaternion(1, 0, 0, 0)
        self._velocity = np.array([0, 0, 0], dtype='float32').T
        self._rotational_velocity = np.array([0, 0, 0], dtype='float32')
        self._acceleration = np.array([0, 0, 0], dtype='float32').T
        self._rotational_acceleration = np.array([0, 0, 0], dtype='float32')
        self._props = Props(2.0, 3.0, 2.0, 3.0)
        self._running = True
        self._clock = pygame.time.Clock()
        self._dt = 0.2

    @property
    def params(self):
        with self._lock:
            return self._position, self._orientation

    @property
    def props(self):
        with self._lock:
            return self._props

    @props.setter
    def props(self, p):
        with self._lock:
            self._props = p

    _accels = {
        0: np.array([ 1,  1,  1]).T,
        1: np.array([ 1, -1, -1]).T,
        2: np.array([-1,  1, -1]).T,
        3: np.array([-1, -1,  1]).T
    }

    def _apply_acceleration(self, orientation, props):
        thrust = 0
        self._acceleration = np.array([0, 0, 0], dtype='float32').T
        accel_rotation = np.array([0,0,0], dtype='float32').T
        for i, p in enumerate(props):
            response = Quad._accels[i]
            accel_rotation += p * response
            thrust += p
        rotate = quaternion.as_rotation_matrix(orientation)
        thrust_vector = rotate.dot(np.array([0, 1, 0], dtype='float32').T)
        self._acceleration += thrust * thrust_vector
        gravity_vector = np.array([0, -10, 0], dtype='float32').T
        self._acceleration += gravity_vector
        # self._rotational_acceleration = quaternion.from_euler_angles(accel_rotation[0], accel_rotation[1], accel_rotation[2])

    def _move(self, pos):
        self._velocity += self._acceleration * self._dt
        self._rotational_velocity += self._rotational_acceleration * self._dt
        with self._lock:
            self._position += self._velocity * self._dt
            self._orientation += self._rotational_velocity * self._dt

    def _get_setup(self):
        with self._lock:
            return self._position, self._orientation, self._props

    def run(self):
        while self._running:
            pos, orientation, props = self._get_setup()
            self._apply_acceleration(orientation, props)
            self._move(pos)
            self._clock.tick(50)

    def quit(self):
        self._running = False
