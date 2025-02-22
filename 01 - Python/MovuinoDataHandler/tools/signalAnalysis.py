

import numpy as np

def mean_time(dat):
    """
    Return the mean index of the incoming data
    :param dat:
    :return:
    """
    i_mean = 0
    E_t = 0
    E = 0
    for i in range(len(dat)):
        E_t += i*dat[i]**2
        E += dat[i]**2

    i_mean = int(E_t/E)
    return i_mean