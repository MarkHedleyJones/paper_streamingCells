import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import integrate
import sys

sys.path.append('/home/mark/Dropbox/University/PhD/Workbench/electrodeInterface/')
import lib.plot.formatter
lib.plot.formatter.plot_params['margin']['left'] = 0.09
lib.plot.formatter.plot_params['margin']['bottom'] = 0.15
lib.plot.formatter.plot_params['margin']['right'] = 0.02
lib.plot.formatter.plot_params['margin']['top'] = 0.03
lib.plot.formatter.format(style='IEEE')

def func_toilet(x, start=3000, duration=80, rate=15, max_flow=0.1):
    end = start + duration
    if start < x < start + duration:
        val = max_flow-max_flow*math.exp((x-end)/rate)
        if val < 0:
            val = 0
    else:
        val = 0
    return val


def func_shower(x, start=900, duration=396.0, flow=0.125):
    if start < x < (start + duration):
        val = flow
    else:
        val = 0
    return val

def func_washing(x, start=100, flow=0.133):
    cycle1_start = start
    cycle1_end = cycle1_start + 8.14*60.0
    cycle2_start = cycle1_end + 20*60.0
    cycle2_end = cycle2_start + 8.14*60.0
    
    if cycle1_start < x < cycle1_end:
        val = flow
    elif cycle2_start < x < cycle2_end:
        val = flow
    else:
        val = 0
        
    return val

xs = list(range(60*60))
ys_shower = list(map(func_shower, xs))
ys_toilet = list(map(func_toilet, xs))
ys_washing = list(map(func_washing, xs))

ys_shower = list(map(lambda x: x * 60.0, ys_shower))
ys_toilet = list(map(lambda x: x * 60.0, ys_toilet))
ys_washing = list(map(lambda x: x * 60.0, ys_washing))
xs = list(map(lambda x: x / 60.0, xs))

ax = plt.gca()
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Flow (L/min)')
ax.set_ylim(0,10)
plt.plot(xs,ys_washing, label='Washing machine', linestyle='--')
plt.plot(xs,ys_shower, label='Shower', linestyle=':')
plt.plot(xs,ys_toilet, label='Toilet')
plt.legend(frameon=False, ncol=3)
plt.savefig('graph_profile.pdf', format='pdf')