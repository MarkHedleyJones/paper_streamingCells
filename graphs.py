#! /bin/python2
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

def func_washing(x, start=100, flow=0.122):
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

ys_flow_shower_min = list(map(lambda x: x * 60.0, ys_shower))
ys_flow_toilet_min = list(map(lambda x: x * 60.0, ys_toilet))
ys_flow_washing_min = list(map(lambda x: x * 60.0, ys_washing))
xs_flow_min = list(map(lambda x: x / 60.0, xs))

ax = plt.gca()
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Flow (L/min)')
ax.set_ylim(0,9)
plt.plot(xs_flow_min,ys_flow_washing_min, label='Washing machine', linestyle='-')
plt.plot(xs_flow_min,ys_flow_shower_min, label='Shower', linestyle='--')
plt.plot(xs_flow_min,ys_flow_toilet_min, label='Toilet', linestyle=':')
plt.legend(frameon=False, ncol=3)

# Cant put these on the same axis because the power output isnt linear with flow
# ax2 = plt.gca().twinx()
# ax2.plot(0,0)
# ax2.set_ylim(0, 54.736000000000004)
# ax2.set_ylabel('Power available')


plt.savefig('graph_profile.pdf', format='pdf')

## Calculate the amount of energy in each event

def pressure_loss_MPa(flow_m3_hour):
    # Trend line obtained from fitting a 2-degree polynomial equation to
    # points read of the pressure loss graphic.
    # Flow is given in m^3/h and pressure is in MPa
    return (0.00316*math.pow(flow_m3_hour,2) + 0.00331*flow_m3_hour + 0.00235)

def convert_litrePerSecond_cubicMeterPerHour(litrePerSec):
    litrePerMin = litrePerSec * 60.0
    litrePerHour = litrePerMin * 60.0
    cubicMeterPerHour = litrePerHour / 1000.0
    return cubicMeterPerHour

def convert_cubicMeterPerHour_cubicMeterPerSecond(cubicMeterPerHour):
    return cubicMeterPerHour / 60.0

def convert_MPa_Pa(pressure_MPa):
    return pressure_MPa * 1000000.0

def calc_power(pressure_Pa, flow_cubicMeterPerSecond):
    return flow_cubicMeterPerSecond * pressure_Pa

def flow_to_power(flow_litrePerSecond):
    flow_cubicMeterPerHour = convert_litrePerSecond_cubicMeterPerHour(flow_litrePerSecond)
    flow_cubicMeterPerSecond = convert_cubicMeterPerHour_cubicMeterPerSecond(flow_cubicMeterPerHour)
    pressure_MPa = pressure_loss_MPa(flow_cubicMeterPerHour)
    power_available = calc_power(convert_MPa_Pa(pressure_MPa), flow_cubicMeterPerSecond)
    return power_available

print(flow_to_power(10.0/60.0))



plt.clf()
lib.plot.formatter.format(style='IEEE')
ax = plt.gca()
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Power (Watts)')
ax.set_ylim(0,40)
plt.plot(xs_flow_min,list(map(flow_to_power, ys_washing)), label='Washing machine', linestyle='-')
plt.plot(xs_flow_min,list(map(flow_to_power, ys_shower)), label='Shower', linestyle='--')
plt.plot(xs_flow_min,list(map(flow_to_power, ys_toilet)), label='Toilet', linestyle=':')
plt.legend(frameon=False, ncol=3)
plt.savefig('graph_harvest.pdf', format='pdf')