from netaddr import *
from env import *
import os
from datetime import datetime

class Analyzer():
    def __init__(self, filelist, target, granu):
        self.filelist = filelist# filelist file name 
        # Change addresses into bits
        self.target = target# Tuple of tuples: ((AS, addr4, addr6), (...)) 
        self.granu = granu # Granularity
        self.as_list = []
        self.addr4_list = []
        self.addr6_list = []
        for t in target:
            self.as_list.append(t[0])
            addr4 = IPAddress(t[1]).bits().replace('.', '')
            self.addr4_list.append(addr4)
            addr6 = IPAddress(t[2]).bits().replace(':', '')
            self.addr6_list.append(addr6)
        self.update_count = {}# 1 minute, datetime: (4 update count, 6 update count)

    def parse_update(self):
        filelist = open(self.filelist, 'r')
        for f in filelist.readlines():
            f = f.replace('\n', '')
            print f
            f = open(hdname + f, 'r')
            for line in f.readlines():
                if line == '' or line == '\n':
                    continue
                # Get attribute name and value
                header = line.split(': ')[0]
                try:
                    content = line.split(': ')[1].replace('\n', '')
                except:
                    continue

                if header == 'TIME':
                    dt = datetime.strptime(content, '%Y-%m-%d %H:%M:%S')
                    if self.granu == '1 minute':
                        dt = dt.replace(second = 0, microsecond = 0)
                    elif self.granu == '10 minute': 
                        dt = dt.replace(second = 0, microsecond = 0)
                        mi = (dt.minute / 10) * 10
                        dt = dt.replace(minute = mi)
                    else:
                        pass

                if header == 'FROM':
                    addr = IPAddress(content).bits()
                    if len(addr) > 100:# IPv6 addr
                        addr = addr.replace(':', '')
                    else:# IPv4 addr
                        addr = addr.replace('.', '')
                        
                    if addr in self.addr4_list or addr in self.addr6_list:
                        if dt not in self.update_count.keys():
                            self.update_count[dt] = [0, 0]
                        if addr in self.addr4_list:# if it is interesting DS AS
                            self.update_count[dt][0] += 1
                        elif addr in self.addr6_list:
                            self.update_count[dt][1] += 1

        filelist.close()
        f.close()
        return 0

    def plot(self):
        import matplotlib.pyplot as plt 
        import matplotlib.dates as mpldates
        from matplotlib.dates import HourLocator
        import numpy as np

        dt = self.update_count.keys()
        dt.sort()

        update4_count = []
        update6_count = []

        for key in dt:
            update4_count.append(self.update_count[key][0])
            update6_count.append(self.update_count[key][1])

        left = 0.05
        width = 0.92
        bottom = 0.15
        height = 0.8
        rect_scatter = [left, bottom, width, height]

        plt.figure(1, figsize=(16, 12))

        axScatter = plt.axes(rect_scatter)
        axScatter.plot(dt, update4_count, 'r-')
        axScatter.plot(dt, update6_count, 'b-')

        axScatter.set_xlabel('Datetime')
        myFmt = mpldates.DateFormatter('%m-%d %H%M')
        axScatter.xaxis.set_major_formatter(myFmt)

        axScatter.set_ylabel('Number of updates')
        axScatter.set_yscale('log')

        plt.show()
        return 0
