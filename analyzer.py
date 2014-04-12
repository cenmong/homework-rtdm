from netaddr import *
from env import *
import os
from datetime import datetime
import time 
from update_class import *
from window_class import *

class Analyzer():

    def __init__(self, filelist, target, granu, win_maxsize):
        self.filelist = filelist# filelist file name 
        self.granu = granu # Granularity
        self.as_list = []# Interesting BGP peer AS
        self.addr4_list = []# IP4 addresses of interesting peer
        self.addr6_list = []# IP6 addresses of interesting peer
        self.update_count = {}# {datetime: (4 update count, 6 update count)}
        self.win4 = Window(win_maxsize)# Initialize a window object
        self.win6 = Window(win_maxsize)# Initialize a window object
        # Modify target BGP peer address format into 0s and 1s
        for t in target:
            self.as_list.append(t[0])
            addr4 = IPAddress(t[1]).bits().replace('.', '')
            self.addr4_list.append(addr4)
            addr6 = IPAddress(t[2]).bits().replace(':', '')
            self.addr6_list.append(addr6)

    def parse_update(self):
        filelist = open(self.filelist, 'r')
        for f in filelist.readlines():
            f = f.replace('\n', '')
            print f
            self.win4.cut_trie()
            self.win6.cut_trie()
            f = open(hdname + f, 'r')
            update_chunk = ''
            for line in f.readlines():
                if line == '':
                    continue
                elif line == '\n':
                    if update_chunk == '':# Game start
                        continue
                    else:
                        updt = Update(update_chunk)
                        from_ip = updt.get_from_ip()
                        if from_ip in self.addr4_list:
                            self.win4.add(updt)
                        elif from_ip in self.addr6_list:
                            self.win6.add(updt)
                        update_chunk = ''
                else:        
                    update_chunk += line.replace('\n', '') + '@@@'
                '''
                # Get attribute name and value
                header = line.split(': ')[0]
                try
                    content = line.split(': ')[1].replace('\n', '')
                except:
                    continue

                if header == 'TIME':
                    dt = datetime.strptime(content, '%Y-%m-%d %H:%M:%S')
                    dt_s = time.mktime(dt.timetuple())# Datetime in seconds
                    # Get datetime object of a specific granularity
                    if self.granu == '1 minute':
                        dt_gra = dt.replace(second = 0, microsecond = 0)
                    elif self.granu == '10 minute': 
                        dt_gra = dt.replace(second = 0, microsecond = 0)
                        mi = (dt_gra.minute / 10) * 10
                        dt_gra = dt_gra.replace(minute = mi)
                    else:
                        pass

                if header == 'FROM':
                    addr = IPAddress(content).bits()
                    # Address format modification
                    if len(addr) > 100:# IPv6 addr
                        addr = addr.replace(':', '')
                    else:# IPv4 addr
                        addr = addr.replace('.', '')

                    # If this is from our interested BGP peer IP
                    if addr in self.addr4_list or addr in self.addr6_list:
                        if dt_gra not in self.update_count.keys():
                            self.update_count[dt_gra] = [0, 0]
                        if addr in self.addr4_list:# if it is our interesting
                            # BGP peer v4 address 
                            self.update_count[dt_gra][0] += 1
                        elif addr in self.addr6_list:# if it is our interesting
                            # BGP peer v6 address 
                            self.update_count[dt_gra][1] += 1'''
            
        filelist.close()
        f.close()
        return 0

    def plot_update_count(self):
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

    def plot_bgp_dynamic(self):
        all4 = self.win4.wadi + self.win4.aadi + self.win4.wwdu +\
        self.win4.aadut1 + self.win4.aadut2 + self.win4.wadu + self.win4.aw
        print self.win4.wadi, ':', float(self.win4.wadi)/float(all4) * 100, '%'
        print self.win4.aadi, ':', float(self.win4.aadi)/float(all4) * 100, '%'
        print self.win4.wwdu, ':', float(self.win4.wwdu)/float(all4) * 100, '%'
        print self.win4.aadut1, ':', float(self.win4.aadut1)/float(all4) * 100, '%'
        print self.win4.aadut2, ':', float(self.win4.aadut2)/float(all4) * 100, '%'
        print self.win4.wadu, ':', float(self.win4.wadu)/float(all4) * 100, '%'
        print self.win4.aw, ':', float(self.win4.aw)/float(all4) * 100, '%'
        all6 = self.win6.wadi + self.win6.aadi + self.win6.wwdu +\
        self.win6.aadut1 + self.win6.aadut2 + self.win6.wadu + self.win6.aw
        print self.win6.wadi, ':', float(self.win6.wadi)/float(all6) * 100, '%'
        print self.win6.aadi, ':', float(self.win6.aadi)/float(all6) * 100, '%'
        print self.win6.wwdu, ':', float(self.win6.wwdu)/float(all6) * 100, '%'
        print self.win6.aadut1, ':', float(self.win6.aadut1)/float(all6) * 100, '%'
        print self.win6.aadut2, ':', float(self.win6.aadut2)/float(all6) * 100, '%'
        print self.win6.wadu, ':', float(self.win6.wadu)/float(all6) * 100, '%'
        print self.win6.aw, ':', float(self.win6.aw)/float(all6) * 100, '%'
