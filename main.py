from analyzer import *

filelist = 'metadata/test-route-views.isc2014.03'
target = ((5580, '198.32.176.206', '2001:504:D::5580:1'),
        (14361, '198.32.176.10', '2001:504:D::1:4361:1'),
        (6939, '198.32.176.20', '2001:504:d::10'),
        (8218, '198.32.176.95', '2001:504:D::5f'),
        (36351, '198.32.176.207', '2001:504:D::3:6351:1'),)

ana = Analyzer(filelist, target, '10 minute')
ana.parse_update()
ana.plot()
