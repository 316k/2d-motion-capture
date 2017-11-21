#!/usr/bin/python3
import pygame, math, sys
from pygame.locals import *
from time import time
from skeleton import Bone
from math import pi
from copy import deepcopy

w, h = 1024, 768
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("wat")

start_time = time()

clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

bkg = WHITE

position = (w/2, 300)
body_height = 200

skeleton = Bone(body_height, position)

# Head
head = Bone(100, (0, 10))
skeleton.add_child(head)

# Left arm
left_arm = Bone(83, (-60, 15))
left_arm.color = RED
skeleton.add_child(left_arm)

left_hand = Bone(83, (0, 83))
left_hand.color = GREEN
left_arm.add_child(left_hand)

# Right arm
right_arm = Bone(83, (60, 15))
right_arm.color = RED
skeleton.add_child(right_arm)

right_hand = Bone(83, (0, 83))
right_hand.color = GREEN
right_arm.add_child(right_hand)

def addv(u, v):
    return tuple((i + j for i, j in zip(u, v)))

def multv(c, v):
    return tuple((c * i for i in v))

def to_deg(rad):
    return rad * 180 / pi

def int_t(t):
    return (int(t[0]), int(t[1]))

def draw_bone(b, images=None):

    start = b.position_start()
    end = b.position_end()

    middle = multv(1/2, addv(end, start))

    if images is not None:
        img = images[0]
        images = images[1:]

        rotation = b.rotation_totale()
        rotated = pygame.transform.rotate(img, -to_deg(rotation))

        rect = rotated.get_rect()
        rect.center = middle

        screen.blit(rotated, rect)
    #else:
    # pygame.draw.aaline(screen, b.color, start, end, 2)

    # pygame.draw.circle(screen, BLUE, int_t(start), 3)
    # pygame.draw.circle(screen, RED, int_t(end), 3)

    for c in b.children:
        if images is not None:
            images = draw_bone(c, images)
        else:
            draw_bone(c)

    return images


def comb_lin(alpha, a, b):
    return list((1 - alpha) * x + alpha * y for x, y in zip(a, b))

def animate(skeleton, init_config, keyframes, images=None):

    orig_kf = deepcopy(keyframes)
    
    start_time = time()
    t = time()

    skeleton.rotate(init_config)

    previous_time, previous_frame = 0, init_config
    target_time, target_frame = 0, init_config

    if len(keyframes):
        # target keyframe
        target_time, target_frame = keyframes.pop(0)

    while True:
        new_t = time()
        
        since_start = new_t - start_time

        # Si on buste le target_time
        if since_start > target_time:
            previous_time, previous_frame = target_time, target_frame
            if len(keyframes) > 0:
                target_time, target_frame = keyframes.pop(0)
            else:
                # Configuration finale
                skeleton.rotate(target_frame)
                target_time = False
                # keyframes = deepcopy(orig_kf)
                # since_start = new_t
                # previous_time, previous_frame = 0, init_config
                # target_time, target_frame = keyframes.pop(0)


        clock.tick(30)

        screen.fill(bkg)

        if target_time:
            n = (since_start - previous_time) / (target_time - previous_time)
            interpolation = comb_lin(n, previous_frame, target_frame)
            skeleton.rotate(interpolation)

        if images is not None:
            copy = images[:]
            draw_bone(skeleton, copy)
        else:
            draw_bone(skeleton)

        pygame.display.flip()

        t = new_t

#(time,  [body, head, left_arm, left_hand, right_arm, right_hand, ...]),
keyframes = [
    (0.75,   [0.1, pi+pi/16, pi/2, -pi/8, -pi/2, pi/8, 0, 0, 0, 0, 0, 0, 0, 0]), 
    (1.5,   [-0.1, pi-pi/16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 
    (2, [0.1, pi, 0, 0, -pi/2, pi/8, 0, 0, 0, 0, 0, 0, 0, 0]), 
    (2.5,   [0, pi, 0, 0, -pi, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (2.8,   [0, pi, 0, 0, -pi, - 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (3.1,   [0, pi, 0, 0, -pi, + 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (3.4,   [0, pi, 0, 0, -pi, - 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (3.7,   [0, pi, 0, 0, -pi, + 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (4.0,   [0, pi, 0, 0, -pi, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    (4.7,   [0, pi, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
]

image_files = ['body', 'head'] + ['bone'] * 10
images = list(map(lambda x: pygame.image.load('imgs/' + x + '.png'), image_files))

animate(skeleton, [0,pi,0,0,0,0,0,0,0,0,0,0,0,0], keyframes, images)
