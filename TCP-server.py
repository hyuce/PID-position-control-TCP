#!/usr/bin/env python

import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd

import socket                 # Import socket module
import time


s = socket.socket()           # Create a socket object
host = "192.168.43.169" # 192.168.1.105"        # Get local machine name
port = 12345                 # Port
s.bind((host, port))          # Bind to the port
s.listen(5)

c, addr = s.accept()       # Establish connection with client.



class tcpPlot:
    def __init__(self, plotLength = 100, dataNumBytes = 2):
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.rawData = bytearray(dataNumBytes)
        self.data = collections.deque([0] * plotLength, maxlen=plotLength)
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0


    def getTCPData(self, frame, lines, lineValueText, lineLabel, timeText):
        currentTimer = time.clock()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        timeText.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        #value1,  = struct.unpack('f', self.rawData)    # use 'h' for a 2 byte integer
	value = c.recv(1024)
	#print(value)
	value = value[0:5]
	print(value)
 	#print(type(value))
	value = value.decode('UTF-8')
	value = (-1) * float(value)
        self.data.append(value)    # we get the latest data point and append it to our array
        lines.set_data(range(self.plotMaxLength), self.data)
        lineValueText.set_text('[' + lineLabel + '] = ' + str(value))
        # self.csvData.append(self.data[-1])


    def close(self):
        self.isRun = False



def main():

    maxPlotLength = 100
    dataNumBytes = 4        # number of bytes of 1 data point
    s = tcpPlot(maxPlotLength, dataNumBytes)   # initializes all required variables

    # plotting starts below
    pltInterval = 50    # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = maxPlotLength
    ymin = -(100) # 50
    ymax = 100    # 50
    fig = plt.figure()
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Angle Time Graphic')
    ax.set_xlabel("time")
    ax.set_ylabel("Angle")

    lineLabel = 'Angle'
    timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
    lines = ax.plot([], [], label=lineLabel)[0]
    lineValueText = ax.text(0.50, 0.90, '', transform=ax.transAxes)
    anim = animation.FuncAnimation(fig, s.getTCPData, fargs=(lines, lineValueText, lineLabel, timeText), interval=pltInterval)    # fargs has to be a tuple

    plt.legend(loc="upper left")
    plt.show()

    s.close()


if __name__ == '__main__':
    main()
