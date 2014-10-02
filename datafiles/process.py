import os
import sys
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

filenames = os.listdir('.')
filenames = filter(lambda x: x.find('_cold_'),filenames)
# print(filenames)
filenames = filter(lambda x: x[-4:] == '.csv', filenames)
filenames.sort()

pp = PdfPages('all.pdf')

for filename in filenames:
    times = []
    currents = []
    pressures = []
    voltages = []
    powers = []
    with open(filename, 'r') as f:
        header = f.readline()
        line = f.readline()
        while line:
            time, current, voltage, pressure, power = map(float,line.split(','))
            line = f.readline()
            times.append(time)
            if filename.find('currentSweep') != -1:
                current = abs(current)
                power = abs(power)
            currents.append(current)
            voltages.append(voltage)
            pressures.append(pressure)
            powers.append(power)

    plt.clf()
    plt.subplot(4,1,1)
    plt.title(filename[26:-4])

    plt.gca().set_ylabel('Current')
    plt.gca().set_ylim(0,1e-7)
    plt.plot(times, currents, label="Current")
    plt.grid()

    plt.subplot(4,1,2)
    plt.gca().set_ylabel('Voltage')
    plt.gca().set_ylim(0,0.5)
    plt.plot(times, voltages, label="Voltage")
    plt.grid()

    plt.subplot(4,1,3)
    plt.gca().set_ylabel('Pressure')
    plt.gca().set_ylim(0,300)
    plt.plot(times, pressures, label="Pressure")
    plt.grid()

    plt.subplot(4,1,4)
    plt.plot(times, powers, label="Power")
    plt.gca().set_ylim(0,1e-8)
    plt.gca().set_ylabel('Power')
    plt.grid()


    plt.tight_layout()


    plt.savefig(pp, format='pdf')
pp.close()
