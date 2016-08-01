from __future__ import division
import numpy as np
from SimpleNet import SimpleNet
import pygame, sys, random, math

class World(object):
    def __init__(self, screen):
        self.screen = screen
        self.bloops = []
        self.foods = []
        self._seed()

    def _seed(self):
        width, height = self.screen.get_size()
        for i in range(100):
            self.foods.append(Food(self.screen,random.randint(0,width),random.randint(0,height)))
        for i in range(20):
            self.bloops.append(Bloop(self.screen,random.randint(0,width),random.randint(0,height)))

    def draw(self):
        for food in self.foods:
            food.draw()
        for bloop in self.bloops:
            bloop.draw()

    def update(self):
        self._spawnFood()
        self._ageBloops()
        self._updateState()
        self._reproduce()
        self._decide()
        self._integrate()

    def _ageBloops(self):
        to_delete = []
        for bloop in self.bloops:
            if not bloop.age():
                to_delete.append(bloop)
                print "Thus dies a bloop"
        for bloop in to_delete:
            self.bloops.remove(bloop)
            del bloop

    def _spawnFood(self):
        if len(self.foods) < 50:
            width, height = self.screen.get_size()
            self.foods.append(Food(self.screen,random.randint(0,width),random.randint(0,height)))

    def _updateState(self):
        for bloop in self.bloops:
            dist, food = self._findNearestFood(bloop)
            if food and dist < bloop.radius + food.size:
                self._eatFood(bloop, food)
                self._findNearestFood(bloop)


    def _findNearestFood(self, bloop):
        min_dist = 1e300
        closest = None
        for food in self.foods:
            diff = food.pos-bloop.pos
            dist = np.hypot(diff[0], diff[1])
            if dist < min_dist:
                min_dist = dist
                closest = food
        bloop.closest = closest
        bloop.closest_range = closest.pos - bloop.pos
        return min_dist, closest

    def _eatFood(self, bloop, food):
        self.foods.remove(food)
        bloop.health += food.health
        del food

    def _reproduce(self):
        reproduction_chance = 0.001
        if random.random() < reproduction_chance:
            print "Reproduce"

    def _decide(self):
        for bloop in self.bloops:
            bloop.decide()

    def _integrate(self):
        for bloop in self.bloops:
            bloop.integrate()

class Bloop(object):
    def __init__(self, screen, x, y):
        self.pos = np.array([x,y], dtype=np.float32)
        self.screen = screen
        self.closest = None
        self.closest_range = np.array([0,0])
        self.health = 100.0
        self.move = np.array([0,0])

    def draw(self):
        pygame.draw.circle(self.screen, (0, 255, 255), self.pos, self.radius, 0)

    def decide(self):
        mag = np.linalg.norm(self.closest_range)
        if mag:
            self.move = self.closest_range / mag
        else:
            self.move = np.array([0,0])

    def integrate(self):
        self.pos += self.move * self.speed

    @property
    def speed(self):
        return 3 / (1 + np.exp(0.1 * (self.health - 50)))

    @property
    def radius(self):
        return int(max(self.health, 5) / 2)


    def age(self):
        self.health -= 0.1
        if self.health <= 0:
            return False
        return True


class Food(object):
    def __init__(self, screen, x, y):
        self.pos = np.array([x,y])
        self.screen = screen
        self.size = 5
        self.health = 5

    def draw(self):
        pygame.draw.circle(self.screen, (0, 255, 0), self.pos, self.size, 0)

if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024,768))
    clock = pygame.time.Clock()
    world = World(screen)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        screen.fill((245,245,245))
        # for i in range(100):
        world.update()
        world.draw()
        pygame.display.update()
        # clock.tick(30)

