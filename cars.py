import pygame
import math

class Car:

    ROT_VEL = 9
    MAX_SPEED = 4
    ACCELERATION = 0.1

    def __init__(self, x, y, initial_angle, img):
        self.angle = initial_angle
        self.x = x
        self.y = y
        self.speed = 0
        self.img = img

    def move(self):
        if self.speed != 0:
            x_vel = math.sin(math.radians(self.angle))* self.speed
            y_vel = math.cos(math.radians(self.angle))* self.speed

            self.x -= x_vel
            self.y -= y_vel

    def move_forward(self):
        self.speed = min(self.speed + self.ACCELERATION, self.MAX_SPEED)
        self.move()

    def move_backward(self):
        self.speed = max(self.speed - self.ACCELERATION, -self.MAX_SPEED/2)
        self.move()

    def steer_left(self):
        self.angle += self.ROT_VEL

    def steer_right(self):
        self.angle -= self.ROT_VEL

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.angle)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))

        poi = mask.overlap(car_mask, offset)
        return poi

    def hit(self):
        self.speed = -self.speed
        self.move()

    def reduce_speed(self):
        self.speed = max(self.speed - self.ACCELERATION / 2, 0)
        self.move()


    def dist_to_collide(self, mask, new_angle,x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)

        new_angle = self.angle + new_angle
        new_x_vel = math.sin(math.radians(new_angle)) * self.MAX_SPEED
        new_y_vel = math.cos(math.radians(new_angle)) * self.MAX_SPEED

        poi = None
        new_x = self.x
        new_y = self.y

        while poi == None:
            offset = (int(new_x - x), int(new_y - y))
            poi = mask.overlap(car_mask, offset)
            new_x -= new_x_vel
            new_y -= new_y_vel

        return math.hypot(new_x - self.x, new_y - self.y)

    def calc_inputs(self, mask):
        inputs = [self.angle]
        for i in range(-90, 135, 45):
            d = self.dist_to_collide(mask, i)
            inputs.append(d)

        return inputs
