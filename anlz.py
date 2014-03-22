from patricia import *
from netaddr import *
from env import *

'''
f4 = open('/datarv2/rib.20140310.1000', 'r')#IPv4 RIB
f6 = open('/datarv6/rib.20140310.1000', 'r')#IPv6 RIB

as6 = []
#store IPv6 ASes into as6
for line in f4.readlines():

asds = []
#store DS ASes into asds
for line in f6.readlines():
f4.close()
f6.close()
'''

'''
trie4 = trie(None)
#build IPv4 trie
f = open('pfx2as/routeviews-rv2-20140310-1200.pfx2as', 'r')#IPv4 prefix2as
s = f.readline().split()
s_addr = IPAddress(s[0]).bits()
s_addr = s_addr.replace('.', '')
s_addr = s_addr[:int(s[1])]

while 1:
    trie4[s_addr] = s[2]
    try:
        s = f.readline().split()
        s_addr = IPAddress(s[0]).bits()
        s_addr = s_addr.replace('.', '')
        s_addr = s_addr[:int(s[1])]
    except:
        break
f.close()

trie6 = trie(None)
#build IPv6 trie
f = open('pfx2as/routeviews-rv6-20140310-0000.pfx2as', 'r')#IPv6 prefix2as
s = f.readline().split()
s_addr = IPAddress(s[0]).bits()
s_addr = s_addr.replace(':', '')
s_addr = s_addr[:int(s[1])]

while 1:
    trie6[s_addr] = s[2]
    try:
        s = f.readline().split()
        s_addr = IPAddress(s[0]).bits()
        s_addr = s_addr.replace(':', '')
        s_addr = s_addr[:int(s[1])]
    except:
        break
f.close()
'''
# Basic idea: attribute every update to its origin AS (the last one on the AS
# path)

# From 0000 to 2345, 15 as interval
'''
time = []
firsthalf = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
for i in range(10, 25):
    firsthalf.append(str(i))
secondhalf = ['00', '15', '30', '45']
for fh in firsthalf:
    for sh in secondhalf:
        time.append(fh + sh)
'''
ym = yearmonth[0]
dn = yearmonth[1]#number of days

as4all = []# Statistics of the whole month
as6all = []
asbothall = []

as4 = {}#dict of AS lists
as6 = {}
asboth = {}

udn4 = {}# Update number of every day
udn6 = {}

ymdlist = []# Year+month+day strings

# TODO: If output files exist, use them instead of read all files again

#IPv6
filelist = 'metadata/6files' + ym 
#filelist = 'metadata/test6files' + ym 
flist = open(filelist, 'r')

for line in flist.readlines():
    print line
    ymd = line.split('.')[-3]
    if ymd not in ymdlist:
        ymdlist.append(ymd)
        as6[ymd] = []# Initialize a list corresponding to a date
        as4[ymd] = []
        udn4[ymd] = 0
        udn6[ymd] = 0
        asboth[ymd] = []

    f = open(hdname + line.replace('\n', ''), 'r')
    for line in f.readlines():
        if line == '' or line == '\n':
            udn6[ymd] += 1
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
            if asn not in as6all:
                as6all.append(asn)
    f.close()
#IPv4
filelist = 'metadata/4files' + ym 
#filelist = 'metadata/test4files' + ym 
flist = open(filelist, 'r')
for line in flist.readlines():
    print line
    ymd = line.split('.')[-3]

    f = open(hdname + line.replace('\n', ''), 'r')
    for line in f.readlines():
        if line == '' or line == '\n':
            udn4[ymd] += 1
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
            if asn not in as4all:
                as4all.append(asn)
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

# Plot something
as4count = []
as6count = []
asbothcount = []
bin6ratio = []

updates4 = []
updates6 = []

xaxis = []
i = 0
for ymd in ymdlist:
    i += 1
    xaxis.append(i)

for ymd in ymdlist:
    as4count.append(len(as4[ymd]))
    as6count.append(len(as6[ymd]))
    asbothcount.append(len(asboth[ymd]))
    bin6ratio.append(float(len(asboth[ymd]))/float(len(as6[ymd])) * 100)
    updates4.append(udn4[ymd])
    updates6.append(udn6[ymd])

# TODO: store every thing into a file

import matplotlib.pyplot as plt 
import numpy as np

# definitions for the axes
left = 0.04
width = 0.92
bottom = 0.15
height = 0.8
rect_scatter = [left, bottom, width, height]

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
