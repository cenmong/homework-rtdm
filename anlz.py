from patricia import *
from netaddr import *
from env import *
import os

ym = yearmonth[0]
dn = yearmonth[1]#number of days

######variables with daily granularity#####
as4all = []# Statistics of the whole month
as6all = []
asbothall = []

as4 = {}#dict of AS lists
as6 = {}
asboth = {}

udn4 = {}# Update number of every day
udn6 = {}

ymdlist = []# Year+month+day strings

######variables with 15 minutes granularity#####
as4c15 = []# To save memory, use list instead of dict
as6c15 = []
ud4c15 = []
ud6c15 = []
dtlist = []# Date time list

# TODO: If output files exist, use them instead of read all files again

#IPv6
#filelist = 'metadata/6files' + ym 
filelist = 'metadata/test6files' + ym 
flist = open(filelist, 'r')
for line in flist.readlines():
    print line
    ymd = line.split('.')[-3]
    datetime = line.split('.')[-3] + line.split('.')[-2]
    dtlist.append(datetime)
    if ymd not in ymdlist:
        ymdlist.append(ymd)
        as6[ymd] = []# Initialize a list corresponding to a date
        as4[ymd] = []
        udn4[ymd] = 0
        udn6[ymd] = 0
        asboth[ymd] = []

    udcount = 0
    ascount = 0
    aslist = []
    f = open(hdname + line.replace('\n', ''), 'r')
    for line in f.readlines():
        if line == '' or line == '\n':
            udn6[ymd] += 1
            udcount += 1
            continue
        header = line.split(': ')[0]
        try:
            content = line.split(': ')[1]
        except:
            continue
        if header == 'AS_PATH':
            asn = content.split()[-1]
            if asn not in as6[ymd]:
                as6[ymd].append(asn)
            if asn not in aslist:
                aslist.append(asn)
                ascount += 1
            if asn not in as6all:
                as6all.append(asn)

    ud6c15.append(udcount)
    as6c15.append(ascount)
    f.close()
#IPv4
#filelist = 'metadata/4files' + ym 
filelist = 'metadata/test4files' + ym 
flist = open(filelist, 'r')
for line in flist.readlines():
    print line
    ymd = line.split('.')[-3]

    udcount = 0
    ascount = 0
    aslist = []
    f = open(hdname + line.replace('\n', ''), 'r')
    for line in f.readlines():
        if line == '' or line == '\n':
            udn4[ymd] += 1
            udcount += 1
            continue
        header = line.split(': ')[0]
        try:
            content = line.split(': ')[1]
        except:
            continue
        if header == 'AS_PATH':
            asn = content.split()[-1]
            if asn not in as4[ymd]:
                as4[ymd].append(asn)
            if asn not in aslist:
                aslist.append(asn)
                ascount += 1
            if asn not in as4all:
                as4all.append(asn)

    ud4c15.append(udcount)
    as4c15.append(ascount)
    f.close()

for ymd in ymdlist:
    for a in as4[ymd]:
        if a in as6[ymd]:
            asboth[ymd].append(a)

for a in as4all:
    if a in as6all:
        asbothall.append(a)

print 'len(as4all)=',len(as4all)
print 'len(as6all)=',len(as6all)
print 'len(asbothall)=',len(asbothall)

# Store date: ASN information into output files to accelerate future run
'''
fo6 = open('output/6output' + ym, 'a')
fo4 = open('output/4output' + ym, 'a')
fob = open('output/boutput' + ym, 'a')

for ymd in ymdlist:
    fo6.write(ymd + ':')
    for a in as6[ymd]:
        fo6.write(' ' + a)
    fo6.write('\n')
    fo4.write(ymd + ':')
    for a in as4[ymd]:
        fo4.write(' ' + a)
    fo4.write('\n')
    fob.write(ymd + ':')
    for a in asboth[ymd]:
        fob.write(' ' + a)
    fob.write('\n')

fo6.close()
fo4.close()
fob.close()
'''
# Plot something
as4count = []
as6count = []
asbothcount = []
bin6ratio = []

updates4 = []
updates6 = []

xaxis = []# Day granularity
i = 0
for ymd in ymdlist:
    i += 1
    xaxis.append(i)

xaxis2 = []# 15 minutes granularity
i = 0
for dt in dtlist:
    i += 1
    xaxis2.append(i)

for ymd in ymdlist:
    as4count.append(len(as4[ymd]))
    as6count.append(len(as6[ymd]))
    asbothcount.append(len(asboth[ymd]))
    bin6ratio.append(float(len(asboth[ymd]))/float(len(as6[ymd])) * 100)
    updates4.append(udn4[ymd])
    updates6.append(udn6[ymd]) 

# store every thing into a file
if not os.path.exists('output/plotdata' + ym):
    f = open('output/plotdata' + ym, 'a')
    f.write('as4count:')
    for i in range(0, len(ymdlist)):
        f.write(',' + str(as4count[i]))
    f.write('\n')
    f.write('as6count:')
    for i in range(0, len(ymdlist)):
        f.write(',' + str(as6count[i]))
    f.write('\n')
    f.write('asbothcount:')
    for i in range(0, len(ymdlist)):
        f.write(',' + str(asbothcount[i]))
    f.write('\n')
    f.write('bin6ratio:')
    for i in range(0, len(ymdlist)):
        f.write(',' + str(bin6ratio[i]))
    f.write('\n')
    f.write('updates4:')
    for i in range(0, len(ymdlist)):
        f.write(',' + str(updates4[i]))
    f.write('\n')
    f.write('updates6:')
    for i in range(0, len(ymdlist)):
        f.write(',' + str(updates6[i]))
    f.write('\n')
    f.close()

import matplotlib.pyplot as plt 
import numpy as np

# definitions for the axes
left = 0.05
width = 0.92
bottom = 0.15
height = 0.8
rect_scatter = [left, bottom, width, height]

############################################by day as number
plt.figure(1, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axScatter.plot(xaxis, as4count, 'ro-')
axScatter.plot(xaxis, as6count, 'bo-')
axScatter.plot(xaxis, asbothcount, 'go-')

for i, txt in enumerate(as4count):
    axScatter.annotate(txt, (i + 1, as4count[i]))
for i, txt in enumerate(as6count):
    axScatter.annotate(txt, (i + 1, as6count[i]))
for i, txt in enumerate(asbothcount):
    axScatter.annotate(txt, (i + 1, asbothcount[i]))

axScatter.set_xlabel('Date')
axScatter.set_ylabel('Number of origin ASes')
axScatter.set_yscale('log')

ylim = np.max(as4count) + 100
axScatter.set_ylim( (0, ylim) )

plt.xticks(xaxis, ymdlist, rotation=70)
plt.show()

###########################################by day update number
plt.figure(2, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axScatter.plot(xaxis, updates4, 'ro-')
axScatter.plot(xaxis, updates6, 'bo-')

for i, txt in enumerate(updates4):
    axScatter.annotate(txt, (i + 1, updates4[i]))
for i, txt in enumerate(updates6):
    axScatter.annotate(txt, (i + 1, updates6[i]))
axScatter.set_xlabel('Date')
axScatter.set_ylabel('Number of updates')
axScatter.set_yscale('log')

ylim = np.max(updates4) + 100
axScatter.set_ylim( (0, ylim) )

plt.xticks(xaxis, ymdlist, rotation=70)
plt.show()

##########################################by 15 minutes as number
plt.figure(3, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axScatter.plot(xaxis2, as4c15, 'r-')
axScatter.plot(xaxis2, as6c15, 'b-')
# TODO: asbothc15

axScatter.set_xlabel('Datetime')
axScatter.set_ylabel('Number of origin ASes')

ylim = np.max(as4c15) + 100
axScatter.set_ylim( (0, ylim) )

#plt.xticks(xaxis, ymdlist, rotation=70)
plt.show()

###########################################by 15 minutes update number
plt.figure(4, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axScatter.plot(xaxis2, ud4c15, 'r-')
axScatter.plot(xaxis2, ud6c15, 'b-')

axScatter.set_xlabel('Datetime')
axScatter.set_ylabel('Number of updates')

ylim = np.max(ud4c15) + 100
axScatter.set_ylim( (0, ylim) )

#plt.xticks(xaxis, ymdlist, rotation=70)
plt.show()
