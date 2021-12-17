import numpy as np
import serial
import serial.tools.list_ports as coms
import time
from datetime import datetime as dt
from matplotlib import pyplot as plt
import glob
import matplotlib.dates as mdates
from datetime import datetime as dt
from matplotlib.ticker import ScalarFormatter


# This is a program for measuring temperature by using 10k ohm thermistor from Thorlab (TH10K)
# Set up pyplot
plt.figure(1)
ax1 = plt.gca()
plt.gcf().autofmt_xdate()
fmt = mdates.DateFormatter('%d-%m %H:%M')
ax1.xaxis.set_major_formatter(fmt)
color = 'tab:blue'
ax1.set_ylabel('Temperature (C)', color=color)

print('10k thermistor logger')
# Arduino the COM port
ser = serial.Serial('COM4', baudrate = 115200, timeout = 2)
t_cycle = input('Input measurement cycle time (s): ')
print()

# Create text file and print header row
filename = 'thermistor_log_' + dt.now().strftime('%y%d%m_%H%M%S') + '.txt'
np.savetxt(filename, ['time stamp,temperature (C)'], newline='\n', fmt='%s')

# Flush serial buffer before beginning

ser.flushInput()
ser.flushOutput()
Time=[]
Temp=[]

while(1):
    # Query Arduino and receive Arduino ADC reading
    ser.write('?'.encode())
    # there's no need to decode or strip;
    x = ser.readline() # .decode("ansi")# .strip()

    # Calculate thermistor resistance from voltage measurement
    V = 5.0*float(x)/1024
    R25 = 1e4 # Resistance at room temperature of thermistor
    Rt = R25*V/(5 - V)

    # Get temperature from thermistor resistance (using Thorlabs data)
    if Rt >= 187 and Rt <= 681.6:
        a,b,c,d = 3.3536166E-03,2.5377200E-04,8.5433271E-07,-8.7912262E-08
    elif Rt > 681.6 and Rt <= 3599:
        a,b,c,d = 3.3530481E-03,2.5420230E-04,1.1431163E-06,-6.9383563E-08
    elif Rt > 3599 and Rt <= 32770:
        a,b,c,d = 3.3540170E-03,2.5617244E-04,2.1400943E-06,-7.2405219E-08
    elif Rt > 32770 and Rt <= 692600:
        a,b,c,d = 3.3570420E-03,2.5214848E-04,3.3743283E-06,-6.4957311E-08
    Tinv = a + b*np.log(Rt/R25) + c*np.log(Rt/R25)**2 + d*np.log(Rt/R25)**3
    T = 1/Tinv - 273.15
    # Print temperature reading and time to terminal window
    time_object = dt.now()
    temp_string = str(np.round(T,2)) + ' C, '
    print('Temperature logged: ' + temp_string + time_object.strftime('%X  %d %b %Y'))
    Time.append(time_object)
    Temp.append(np.round(T,2))
    # Plot graph (real time)
    i_plot=0;
    while(1):
        plt.plot(Time, Temp,'r',label = 'Current Temperature (C)')
        temptext = ax1.text(0.75, 1.08, "Temp = " + str(np.round(Temp[-1],2)) + ' C',color='b',transform = ax1.transAxes)
        plt.draw()
        plt.pause(0.1)
        temptext.remove()
        i_plot=1;
        if i_plot>0: 
            break
    # Pause for user specified time
    time.sleep(float(t_cycle))
