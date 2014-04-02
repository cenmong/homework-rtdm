from patricia import *
from netaddr import *
from env import hdname
import os

# If import them from get_special_file.py, then the py file will unnecessarily run again.
ym = ['2003.08', '2005.09', '2005.08', '2006.12', '2008.01', '2008.12', '2011.03']
ymd1 = ['20030814', '20050911', '20050829', '20061226', '20080130', '20081219',
     '20110310']
ymd2 = ['20030815', '20050912', '20050830', '20061227', '20080131', '20081220',
     '20110311']

fig_n = 1
for i in range(6, len(ym)):
    dt60list4 = []# store each hour
    dt60list6 = []#
    ######variables with hour granularity#####
    as4c60 = []# To save memory, use list instead of dict
    as6c60 = []
    ud4c60 = []
    ud6c60 = []
    as4_60 = {} # Store each AS number
    as6_60 = {}
    asbothc60 = []

    # IPv6
    dt60 = ''
    udcount60 = 0
    flist = open('metadata/6files' + ymd1[i], 'r')
    for line in flist.readlines():
        print line
        # Get year-month-day-time strings from files name
        ymd = line.split('.')[-3]
        datetime = line.split('.')[-3] + line.split('.')[-2]

        old_dt60 = dt60
        dt60 = datetime[:10]# Get hour information from full time string
        if dt60 not in dt60list6:# If this hour has not been stored before
            dt60list6.append(dt60)# Then store it and 
            as6_60[dt60] = []# Initialize a new list in a AS 6 dict of hour
            if old_dt60 != '':# If get a new dt60 and it is not the first one
                ud6c60.append(udcount60)
                udcount60 = 0
                as6c60.append(len(as6_60[old_dt60]))

        f = open(hdname + line.replace('\n', ''), 'r')
        for l in f.readlines():
            if l == '' or l == '\n':
                udcount60 += 1
                continue
            header = l.split(': ')[0]
            try:
                content = l.split(': ')[1]
            except:
                continue
            if header == 'AS_PATH':
                asn = content.split()[-1]
                if asn not in as6_60[dt60]:
                    as6_60[dt60].append(asn)

        f.close()
    ud6c60.append(udcount60)
    as6c60.append(len(as6_60[dt60]))
    
    # IPv4
    udcount60 = 0
    dt60 = ''
    flist = open('metadata/4files' + ymd1[i], 'r')
    for line in flist.readlines():
        print line
        datetime = line.split('.')[-3] + line.split('.')[-2]

        old_dt60 = dt60
        dt60 = datetime[:10]
        if dt60 not in dt60list4:
            dt60list4.append(dt60)
            as4_60[dt60] = []
            if old_dt60 != '':# If get a new dt60 and it is not the first one
                ud4c60.append(udcount60)
                udcount60 = 0
                as4c60.append(len(as4_60[old_dt60]))

        f = open(hdname + line.replace('\n', ''), 'r')
        for l in f.readlines():
            if l == '' or l == '\n':
                udcount60 += 1
                continue
            header = l.split(': ')[0]
            try:
                content = l.split(': ')[1]
            except:
                continue
            if header == 'AS_PATH':
                asn = content.split()[-1]
                if asn not in as4_60[dt60]:
                    as4_60[dt60].append(asn)

        f.close()
    ud4c60.append(udcount60)
    as4c60.append(len(as4_60[dt60]))

    print len(dt60list4)
    print len(dt60list6)
    print len(as4c60)
    print len(as6c60)

    ############################################## Plot something
    xaxis60 = []# hour granularity
    i = 0
    for dt in dt60list4:
        i += 1
        xaxis60.append(i)

    import matplotlib.pyplot as plt 
    import numpy as np

    # definitions for the axes
    left = 0.05
    width = 0.92
    bottom = 0.15
    height = 0.8
    rect_scatter = [left, bottom, width, height]
    ##########################################by 60 minutes origin AS count
    plt.figure(fig_n, figsize=(16, 12))
    fig_n += 1

    axScatter = plt.axes(rect_scatter)
    axScatter.plot(xaxis60, as4c60, 'r-')
    axScatter.plot(xaxis60, as6c60, 'b-')
    #axScatter.plot(xaxis60, asbothc60, 'g-')

    axScatter.set_xlabel('Datetime')
    axScatter.set_ylabel('Number of origin ASes')
    axScatter.set_yscale('log')

    plt.show()

    ###########################################by 60 minutes update count
    plt.figure(fig_n, figsize=(16, 12))
    fig_n += 1

    axScatter = plt.axes(rect_scatter)
    axScatter.plot(xaxis60, ud4c60, 'r-')
    axScatter.plot(xaxis60, ud6c60, 'b-')

    axScatter.set_xlabel('Datetime')
    axScatter.set_ylabel('Number of updates')
    axScatter.set_yscale('log')

    plt.show()
