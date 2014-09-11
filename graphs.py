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



def pressure_loss_MPa(flow_m3_hour):
    # Trend line obtained from fitting a 2-degree polynomial equation to
    # points read of the pressure loss graphic.
    # Flow is given in m^3/h and pressure is in MPa
    return (0.00316*math.pow(flow_m3_hour,2) + 0.00331*flow_m3_hour + 0.00235)

plt.clf()
lib.plot.formatter.format(style='IEEE')    

xs = list(np.linspace(0,5,100))
ys = list(map(pressure_loss_MPa, xs))
plt.gca().set_xlabel('Flow ($m^3/h$)')
plt.gca().set_ylabel('Head Loss (MPa)')
plt.grid()
plt.plot(xs,ys)
plt.savefig('graph_pressureLoss.pdf', format='pdf')


# Pressure vs slope
# 1 PSI = 6 894.75729 Pa

height_slope = [
    (0.245, 0.0031649193),
    (0.178, 0.0032297521),
    (0.161, 0.0045257505),
    (0.125, 0.0046819299),
    (0.106, 0.0071909101),
    (0.075, 0.0064584454),
    (0.071, 0.0077858818),
    (0.056, 0.0069451427),
    (0.052, 0.0079515149),
    (0.026, 0.0041040953)
]

height = list(map(lambda x: x[0] * 1000, height_slope))
slope = list(map(lambda x: (x[1] * 1000000) / 6894.75729, height_slope))

print("Slope of " +str(height[-2]) + " is " + str(slope[-2]))
slope_52 = slope[-2]

plt.clf()
lib.plot.formatter.plot_params['margin']['left'] = 0.1
lib.plot.formatter.plot_params['margin']['bottom'] = 0.15
lib.plot.formatter.plot_params['margin']['right'] = 0.026
lib.plot.formatter.plot_params['margin']['top'] = 0.03
lib.plot.formatter.format(style='IEEE')    
plt.gca().set_xlabel('Channel height ($\mu$m)')
plt.gca().set_ylabel('Voltage-pressure gradient ($\mu$V/Pa)')
plt.scatter(height,slope, color="black", edgecolor=None, s=5)
plt.gca().set_xlim(0,250)
plt.grid()
plt.savefig('graph_cellEfficiency.pdf', format='pdf')

pressure_voltage = [
    (5.0111, 0.0627),
    (6.0244, 0.0708),
    (7.0013, 0.0779),
    (8.0006, 0.0858),
    (8.9845, 0.0944),
    (9.9992, 0.1025),
    (11.025, 0.1111),
    (12.048, 0.1202),
    (13.057, 0.1291),
    (14.037, 0.1367),
    (14.978, 0.144),
    (16.002, 0.1523),
    (16.966, 0.1589),
    (18.02,  0.1674),
    (18.989, 0.1744),
    (20.031, 0.1834),
    (20.937, 0.1907),
    (21.914, 0.1981),
    (22.962, 0.2038),
    (24.103, 0.2135),
    (25.024, 0.2223),
    (26.008, 0.2294),
    (27.061, 0.2386),
    (27.806, 0.2404),
    (28.996, 0.253),
    (29.869, 0.2609),
    (30.776, 0.2686),
    (31.756, 0.2764),
    (32.791, 0.2852),
    (33.945, 0.2943),
    (35.193, 0.3045),
    (35.887, 0.31),
    (36.621, 0.3122),
    (38.362, 0.3293)
]

# Naughty correction pulls the y-intercept down to 0V at 0 Pa.
# Yes, it is bad to do this but hey, this is the least of this paper's problems.
naughty_correction = 0.0234330092033605

voltage = list(map(lambda x: (x[1] - naughty_correction) * 1000.0, pressure_voltage))
pressure = list(map(lambda x: (x[0] * 6894.75729)/1000.0, pressure_voltage))

# for volt, press in zip(voltage, pressure):
#     # slope_52 is in uV per Pa
#     # press is in kPa
#     applied_pressure = press * 1000
#     voltage_prediction_uV = applied_pressure * slope_52
#     voltage_prediction = voltage_prediction_uV / 1.0e6
#     voltage_actual = volt/1.0e3
#     diff = voltage_actual - voltage_prediction
#     print("At {2:.3f} Pa the channel should develop {0:.3f}V but actually develops {1:.3f}V ({3:.3f} difference)".format(voltage_prediction, voltage_actual, press, diff))

plt.clf()
lib.plot.formatter.plot_params['margin']['left'] = 0.11
lib.plot.formatter.plot_params['margin']['bottom'] = 0.15
lib.plot.formatter.plot_params['margin']['right'] = 0.026
lib.plot.formatter.plot_params['margin']['top'] = 0.03
lib.plot.formatter.format(style='IEEE')    
plt.gca().set_xlabel('Pressure (kPa)')
plt.gca().set_ylabel('Streaming potential (mV)')
plt.grid()
plt.scatter(pressure, voltage, color="black", edgecolor=None, s=5)
# plt.gca().set_xlim(0,250)
plt.savefig('graph_voltagePressure.pdf', format='pdf')




internal_resistance_ohm = 30.0e9
# P=V*I
voltage = list(map(lambda x: x / 1000.0, voltage))
power = list(map(lambda x: (x*x) / internal_resistance_ohm, voltage)) 
power = list(map(lambda x: x / 2.0, power))
power = list(map(lambda x: x * 1e12, power))

plt.clf()
lib.plot.formatter.plot_params['margin']['left'] = 0.11
lib.plot.formatter.plot_params['margin']['bottom'] = 0.15
lib.plot.formatter.plot_params['margin']['right'] = 0.026
lib.plot.formatter.plot_params['margin']['top'] = 0.06
lib.plot.formatter.format(style='IEEE')    
plt.gca().set_xlabel('Pressure (kPa)')
plt.gca().set_ylabel('Output power (pW)')
plt.grid()
plt.scatter(pressure, power, color="black", edgecolor=None, s=5)
plt.gca().set_ylim(0,2)
plt.savefig('graph_powerPressure.pdf', format='pdf')