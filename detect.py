#!/usr/bin/python3

import math
import cv2
import numpy as np

from functools import reduce

def open_gray(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray

def test_find_lines(gray, gauss_width=1, closings=0, erosions=0):

    # Upscale (x2) that image
    gauss = gray.copy()
    er = gray.copy()
    canny = gray.copy()
    closing = gray.copy()

    kernel = np.array((3,3),np.uint8)

    gauss_width = 3
    gauss = cv2.GaussianBlur(gray, (gauss_width, gauss_width), 0)
    cv2.imshow("Gauss", gauss)
    gray=gauss

    # closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=closings)
    # cv2.imshow("Closing", closing)
    # gray = closing

    # er = cv2.erode(gray, kernel, iterations=erosions)
    # cv2.imshow("Erosions", er)
    # gray = er

    # canny = cv2.Canny(gray, 40, 100, None, 3)
    # cv2.imshow("Canny", canny)
    # gray = canny

    lines = cv2.HoughLinesP(gray, 1, math.pi/180, 80, None, 30)

    # cv2.waitKey()
    # return []

    # Visualisation


    a,b,c = lines.shape

    hough = np.zeros((gray.shape[0], gray.shape[1], 3))

    colors = [(0,0,255),(255,0,0), (0,255,0), (255,255,0), (0,255,255)]
    for i in range(a):
        cv2.line(hough, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), colors[i % len(colors)], 1, cv2.LINE_AA)

    cv2.imshow("Hough", hough)
    cv2.waitKey()

    # Pas sûr de si ça peut changer, mais le return en dépend
    assert lines.shape[1] == 1

    return lines[:,0]

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def vector_norm(x):
    return math.sqrt(x[0]**2 + x[1] ** 2)

def vector_distance(u, v):
    return math.sqrt(reduce(lambda acc, pair: acc + (pair[0] - pair[1])**2, zip(u, v), 0))

def almost_same_as(line, lines, tresh_norm=0.01, tresh_dist=10):
    """Garde seulement les lignes qui sont pratiquement parallèles et très
    proches d'une ligne donnée

    """
    pts1 = [(line[0], line[1]), (line[2], line[3])]
    n1 = normalized(np.array([line[2] - line[0], line[3] - line[1]]))[0]
    m1 = n1[0]/n1[1] # Δy/Δx

    similaires = []
    print("##", line)

    for l in lines:
        pts2 = [(l[0], l[1]), (l[2], l[3])]
        n2 = normalized(np.array([l[2] - l[0], l[3] - l[1]]))[0]
        m2 = n2[0]/n2[1] # Δy/Δx

        m = (m1 + m2)/2

        b1 = line[1]/(m*line[0])
        b2 = l[1]/(m*l[0])

        d = abs(b2 - b1)/math.sqrt(m1**2 + 1)

        if 1 - np.dot(n1, n2) < tresh_norm: # and d < tresh_dist:
            print(" take", l, ":", 1 - np.dot(n1, n2), " and ", d)
            similaires.append(l)
        else:
            print(" not", l, ":", 1 - np.dot(n1, n2), " and ", d)

    return similaires

def choose_best_lines(lines):
    """
    Trouver les lignes les plus longues, avec le
    moins de lignes parallèles proches
    """
    lines = set(map(tuple, lines))
    best = []

    while len(lines) > 0:
        # pick une ligne
        l = lines.pop()
        # prend tout ce qui est similaire
        similaires = set(almost_same_as(l, lines))
        # retire les deux groupes du set
        lines = lines.difference(similaires)

        longest = reduce(lambda acc, x: x if vector_norm(x) > vector_norm(acc) else acc, similaires.union([l]))

        # met dans best la meilleur ligne du paquet (biggest norm())
        best.append(longest)

    return best

def show_lines(img, lines):
    out = np.zeros((img.shape[0], img.shape[1], 3))

    colors = [(0,0,255),(255,0,0), (0,255,0), (255,255,0), (0,255,255)]
    for i, l in enumerate(lines):
        cv2.line(out, (l[0], l[1]), (l[2], l[3]), colors[i % len(colors)], 1, cv2.LINE_AA)

    cv2.imshow("Lines", out)
    cv2.waitKey()


def find_lines(gray):

    # Upscale (x2) that image
    gauss = gray.copy()
    er = gray.copy()
    canny = gray.copy()
    closing = gray.copy()

    kernel = np.array((3,3),np.uint8)

    gauss_width = 3
    gauss = cv2.GaussianBlur(gray, (gauss_width, gauss_width), 0)
    # cv2.imshow("Gauss", gauss)
    gray=gauss

    lines = cv2.HoughLinesP(gray, 1, math.pi/180, 80, None, 30)

    # cv2.waitKey()
    # return []

    # Visualisation


    a,b,c = lines.shape

    hough = np.zeros((gray.shape[0], gray.shape[1], 3))

    colors = [(0,0,255),(255,0,0), (0,255,0), (255,255,0), (0,255,255)]
    for i in range(a):
        cv2.line(hough, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), colors[i % len(colors)], 1, cv2.LINE_AA)

    # cv2.imshow("Hough", hough)
    #cv2.waitKey()

    # Pas sûr de si ça peut changer, mais le return en dépend
    assert lines.shape[1] == 1

    return lines[:,0]


if __name__ == "__main__":

    # for i in (1,2,3):
    #     img = open_gray('sk/' + str(i) + 'n.png')
    #     lines = find_lines(img)
    #     print(len(lines), lines, end='\n\n')

    img = open_gray('sk/4n.png')

    maybe = find_lines(img)
    show_lines(img, maybe)

    best = choose_best_lines(maybe)
    show_lines(img, best)

    print('\n'.join(map(str, best)))
