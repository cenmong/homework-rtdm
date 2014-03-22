import os 
from env import *

# TODO: Some empty parsed files at the begining! At that time the system cannot
# find the file for catting
####################################IPv6#####################################
# Download files
ym = yearmonth[0]
os.system('wget -e robots=off --connect-timeout=3000 -np -P ' + hdname + ' -c -m -r -A.bz2\
        http://archive.routeviews.org/route-views6/bgpdata/' + ym +\
        '/UPDATES/')
# Get file list
os.system('lynx -dump http://archive.routeviews.org/route-views6/bgpdata/' + ym +\
        '/UPDATES/ > filehtml6')
f = open('filehtml6', 'r')
if os.path.exists('metadata/6files' + ym):
    os.system('rm metadata/6files' + ym)
flist = open('metadata/6files' + ym, 'a')
for line in f.readlines():
    if line.split('.')[-1] != 'bz2\n':
        continue
    topofile = line.split('//')[1]
    flist.write(topofile.replace('.bz2', '.psd'))# Names of parsed files are stored
    topofile = topofile.replace('\n', '')
    if os.path.exists(hdname + topofile):
        try:
            os.system('bunzip2 ' + hdname + topofile)#  Unpack the files
        except:
            pass
    topofile = topofile.replace('.bz2', '')
    if os.path.exists(hdname + topofile):
        try:
            os.system('cat ' + hdname + topofile + ' | time\
                    ~/Downloads/zebra-dump-parser/zebra-dump-parser.pl > ' + hdname + topofile +\
                    '.psd')# Parse files using zebra parser
        except:
            pass
    if os.path.exists(hdname + topofile + '.psd'):# Parsed files exist
        try:
            os.system('rm ' + hdname + topofile)# Remove unparsed files
        except:# File has already been removed
            pass

f.close()
flist.close()
os.system('rm filehtml6')
####################################IPv4#####################################
# Download files
ym = yearmonth[0]
os.system('wget -e robots=off --connect-timeout=3000 -np -P ' + hdname + ' -c -m -r -A.bz2\
        http://archive.routeviews.org/bgpdata/' + ym +\
        '/UPDATES/')
# Get file list
os.system('lynx -dump http://archive.routeviews.org/bgpdata/' + ym +\
        '/UPDATES/ > filehtml4')
f = open('filehtml4', 'r')
if os.path.exists('metadata/4files' + ym):
    os.system('rm metadata/4files' + ym)
flist = open('metadata/4files' + ym, 'a')
for line in f.readlines():
    if line.split('.')[-1] != 'bz2\n':
        continue
    topofile = line.split('//')[1]
    flist.write(topofile.replace('.bz2', '.psd'))# Names of parsed files are stored
    topofile = topofile.replace('\n', '')
    if os.path.exists(hdname + topofile):
        try:
            os.system('bunzip2 ' + hdname + topofile)#  Unpack the files
        except:
            pass
    topofile = topofile.replace('.bz2', '')
    if os.path.exists(hdname + topofile):
        try:
            os.system('cat ' + hdname + topofile + ' | time\
                    ~/Downloads/zebra-dump-parser/zebra-dump-parser.pl > ' + hdname + topofile +\
                    '.psd')# Parse files using zebra parser
        except:
            pass
    if os.path.exists(hdname + topofile + '.psd'):# Parsed files exist
        try:
            os.system('rm ' + hdname + topofile)# Remove unparsed files
        except:# File has already been removed
            pass

f.close()
flist.close()
os.system('rm filehtml4')
