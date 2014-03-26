import os
from env import hdname

ym = ['2003.08', '2005.09', '2005.08', '2006.12', '2008.01', '2008.12']

ymd1 = ['20030814', '20050911', '20050829', '20061226', '20080130', '20081219']

ymd2 = ['20030815', '20050912', '20050830', '20061227', '20080131', '20081220']

# IPv6
for i in range(0, len(ym)):
    os.system('lynx -dump http://archive.routeviews.org/route-views6/bgpdata/' + ym[i] +\
            '/UPDATES/ > filehtml6')
    f = open('filehtml6', 'r')
    if os.path.exists('metadata/6files' + ymd1[i]):
        os.system('rm metadata/6files' + ymd1[i])
    flist = open('metadata/6files' + ymd1[i], 'a')
    for line in f.readlines():
        if line.split('.')[-1] != 'bz2\n':
            continue
        if line.split('.')[-3] != ymd1[i] and line.split('.')[-3] != ymd2[i]:
            continue
        topofile = line.split('//')[1]
        topofile = topofile.replace('\n', '')
        # Download files
        if not os.path.exists(hdname + topofile.replace('bz2', 'psd')):
            os.system('wget -e robots=off --connect-timeout=3000 -np -P ' + hdname + ' -c -m -r -A.bz2\
                    http://' + topofile)
        else:
            continue
        flist.write(topofile.replace('.bz2', '.psd') + '\n')# Names of parsed files are stored
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

# IPv4
for i in range(0, len(ym)):
    os.system('lynx -dump http://archive.routeviews.org/bgpdata/' + ym[i] +\
            '/UPDATES/ > filehtml4')
    f = open('filehtml4', 'r')
    if os.path.exists('metadata/4files' + ymd1[i]):
        os.system('rm metadata/4files' + ymd1[i])
    flist = open('metadata/4files' + ymd1[i], 'a')
    for line in f.readlines():
        if line.split('.')[-1] != 'bz2\n':
            continue
        if line.split('.')[-3] != ymd1[i] and line.split('.')[-3] != ymd2[i]:
            continue
        topofile = line.split('//')[1]
        topofile = topofile.replace('\n', '')
        # Download files
        if not os.path.exists(hdname + topofile.replace('bz2', 'psd')):
            os.system('wget -e robots=off --connect-timeout=3000 -np -P ' + hdname + ' -c -m -r -A.bz2\
                    http://' + topofile)
        else:
            continue
        flist.write(topofile.replace('.bz2', '.psd') + '\n')# Names of parsed files are stored
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
