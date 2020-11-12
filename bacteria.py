import arcade
import random
import math
import numpy as np
from conf import *


class Bacterias(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        for i in range(BACTERIA_COUNT):
            self.append(Bacteria())

    def update(self, delta_time):
        for sprite in self:
            sprite.update(delta_time)


class Bacteria(arcade.Sprite):
    def __init__(self, parent=None, zuper=False):
        # Create the bacterias
        super().__init__("sprites/bacteria.png", SPRITE_SCALING_FOOD)

        angle = random.uniform(0, 2*math.pi)
        self.angle = math.degrees(angle)
        # self.change_x = math.cos(angle) * self.speed
        # self.change_y = math.sin(angle) * self.speed
        self.weight = 1#np.random.uniform(min_weight, 1)
        self.speed = 3/math.sqrt(self.weight)#np.random.uniform(1, 2)
        #self.speed = np.random.uniform(1, 2)

        # brain initialisation
        self.inputs = 9
        self.hidden = 5
        self.output = 3
        sigma = 0.1
        if parent is None:
            self.W1 = sigma*np.random.randn(self.hidden, self.inputs + 1)
            self.W2 = sigma*np.random.randn(self.output, self.hidden + 1)
            self.W3 = sigma*np.random.randn(self.output, self.inputs + 1)
            self.center_x = random.randrange(SCREEN_WIDTH)
            self.center_y = random.randrange(SCREEN_HEIGHT)

            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.W1 = parent.W1 + 0.01 * np.random.randn(*np.shape(parent.W1)) * parent.W1
            self.W2 = parent.W2 + 0.01 * np.random.randn(*np.shape(parent.W2)) * parent.W2
            self.W3 = parent.W3 + 0.01 * np.random.randn(*np.shape(parent.W3)) * parent.W3
            self.center_x = parent.center_x + random.randint(-20, 20)
            self.center_y = parent.center_x + random.randint(-20, 20)
            # self.center_x = random.randrange(SCREEN_WIDTH)
            # self.center_y = random.randrange(SCREEN_HEIGHT)
            # self.speed = parent.speed
            self.color = parent.color

        self.zuper = zuper
        if zuper:
            self.W3 = np.zeros_like(self.W3)
            self.W3[0][4] = 1
            self.W3[1][5] = 1
            print(self.W3)

    def update(self, delta_time):
        #self.angle = self.angle + 1
        self.change_x = math.cos(math.radians(self.angle)) * math.log(self.speed)
        self.change_y = math.sin(math.radians(self.angle)) * math.log(self.speed)
        self.weight -= 0.1 * delta_time
        if self.weight < min_weight:
            self.remove_from_sprite_lists()
        self.speed = 3/math.sqrt(self.weight)
        self.scale = SPRITE_SCALING_BACTERIA * math.log(2 + self.weight)
        super().update()

    def collision_with_bacteria(self, bacteria):
        if self.weight > bacteria.weight:
            self.weight += 0.8*bacteria.weight
            bacteria.remove_from_sprite_lists()
        else:
            bacteria.weight += 0.8*self.weight
            self.remove_from_sprite_lists()

    def collision_with_food(self, food):
        self.weight += 0.1
        food.remove_from_sprite_lists()

    def dist_to(self, smthing):
        if not smthing is None:
            return np.linalg.norm([self.center_x - smthing.center_x, self.center_y - smthing.center_y])
        else:
            return SCREEN_WIDTH**2 + SCREEN_HEIGHT**2

    def forward_pass(self, nearest_bacteria, nearest_food):
        if nearest_bacteria is None:
            nearest_bacteria = type('nearest_bacteria', (), {})()
            setattr(nearest_bacteria, 'center_x', -SCREEN_WIDTH)
            setattr(nearest_bacteria, 'center_y', -SCREEN_HEIGHT)
            setattr(nearest_bacteria, 'weight', 0)
            setattr(nearest_bacteria, 'speed', 0)

        if nearest_food is None:
            nearest_food = type('nearest_food', (), {})()
            setattr(nearest_food, 'center_x', -SCREEN_WIDTH)
            setattr(nearest_food, 'center_y', -SCREEN_HEIGHT)
            setattr(nearest_food, 'weight', 0)
            setattr(nearest_food, 'speed', 0)

        inp = np.array([(nearest_bacteria.center_x - self.center_x)/100,
                        (nearest_bacteria.center_y - self.center_y)/100,
                        nearest_bacteria.weight,
                        nearest_bacteria.speed,
                        (nearest_food.center_x - self.center_x)/100,
                        (nearest_food.center_y - self.center_y)/100,
                        self.weight,
                        self.speed,
                        (self.angle%360)/360,
                        1])

        # h = np.dot(self.W1, inp)
        # h = 1/(1 + np.exp(-h))
        # h = np.concatenate((h, [1]))
        # output = np.dot(self.W2, h)
        output = np.dot(self.W3, inp)

        # if self.zuper:
        #     print(inp)
            # print(output)

        output = 1/(1 + np.exp(-output))
        output = 2*output-1
        norm = np.linalg.norm(output[:2])
        output /= norm
        # if self.zuper:
        #     print(output)
        angle = math.atan2(output[1], output[0])
        self.angle = math.degrees(angle)
        # if self.zuper:
        #     print(self.angle)
        self.priorities = output[2]
