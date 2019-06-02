import numpy as np
from random import sample as rnd_sample
from .GlobalVariable import *

def user_vec(areas, history):
    # areas -> 'a,b,c' filled at reg
    # history -> 'field(s) date'
    # future: user.fav__proj__area
    #          all projects' tags
    focus = np.zeros(len(AREA_CHOICES), dtype=int)
    areas = areas.split(',')
    for a in areas:
        focus[int(a)] = 10
    for h in history:
        areas = h[0].split(',')
        for a in areas:
            focus[int(a)] += 1

    return focus


def area_dist(user_area, proj_area):
    pa = np.zeros(len(AREA_CHOICES), dtype=int)
    for a in proj_area:
        pa[int(a)] = 1
    return np.linalg.norm(pa - user_area)


rec_before_sample = 20
rec_num = 4
def recommend(areas, history, all_proj):
    dist_list = [-1.0]*20
    rec_list = [None for i in range(rec_before_sample)]

    focus = user_vec(areas, history)
    next_insert_index = 0
    for p in all_proj:
        areas = p.area.split(',')
        d = area_dist(focus, areas)
        if -1.0 in dist_list:
            rec_list[next_insert_index] = p
            dist_list[next_insert_index] = d
            if -1.0 in dist_list:
                next_insert_index += 1
            else:
                next_insert_index = np.argmax(dist_list)
        else:
            if d < dist_list[next_insert_index]:
                rec_list[next_insert_index] = p
                dist_list[next_insert_index] = d
                next_insert_index = np.argmax(dist_list)
    # print(dist_list, rec_list)
    return rnd_sample(rec_list, rec_num)