import pygame
import sys
from operator import itemgetter
import threading
import numpy as np
import quaternion

from Quad import Quad, runQuad

class Simulation:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.vertices = np.array([
            [-1, 1, -1],
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, 1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1]
        ], dtype='float32')
        self.faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (0, 4, 5, 1), (3, 2, 6, 7)]
        self.colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0)]
        self.angle = 0
        self.quad = Quad()


    def run(self):
        t = threading.Thread(target=runQuad, args=(self.quad,))
        t.start()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quad.quit()
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill((0, 32, 0))

            position, orientation = self.quad.params
            rotation = quaternion.as_rotation_matrix(orientation)
            t = self.vertices.dot(rotation) + position

            factors = 256 / (4 + t[:,2]) # fov / viewer_distance + z
            t[:, 0] =  t[:, 0] * factors + self.screen.get_width() / 2
            t[:, 1] = -t[:, 1] * factors + self.screen.get_height() / 2

            avg_z = []
            for i, f in enumerate(self.faces):
                z = (t[f[0],2] + t[f[1],2] + t[f[2],2] + t[f[3],2]) / 4.0
                avg_z.append([i, z])

            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0],0], t[f[0],1]), (t[f[1],0], t[f[1],1]),
                             (t[f[1],0], t[f[1],1]), (t[f[2],0], t[f[2],1]),
                             (t[f[2],0], t[f[2],1]), (t[f[3],0], t[f[3],1]),
                             (t[f[3],0], t[f[3],1]), (t[f[0],0], t[f[0],1])]
                pygame.draw.polygon(self.screen, self.colors[face_index], pointlist)
            self.angle += 1

            pygame.display.flip()


if __name__ == "__main__":
    Simulation().run()