import pygame
import sys
from operator import itemgetter
import threading

from Point3D import Point3D
from Quad import Quad, runQuad

class Simulation:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.vertices = [
            Point3D(-1, 1, -1),
            Point3D(1, 1, -1),
            Point3D(1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, 1, 1),
            Point3D(1, 1, 1),
            Point3D(1, -1, 1),
            Point3D(-1, -1, 1)
        ]
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

            t = []
            params = self.quad.get_params()

            for v in self.vertices:
                r = v.rotateX(params.rx).rotateY(params.ry).rotateZ(params.rz)
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                t.append(p)

            avg_z = []
            for i, f in enumerate(self.faces):
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i, z])

            for tmp in sorted(avg_z, key=itemgetter(1), reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(self.screen, self.colors[face_index], pointlist)
            self.angle += 1

            pygame.display.flip()


if __name__ == "__main__":
    Simulation().run()