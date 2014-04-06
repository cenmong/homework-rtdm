from update_class import *
from netaddr import *
import patricia

class Window():
    def __init__(self, maxsize, protocol_type):
        self.ptype = protocol_type
        self.maxsize = maxsize
        # IPv4 window parameters
        self.size = 0
        self.start = 0# Window start
        self.end = 0# Window end
        self.trie = patricia.trie(None)# Store still active updates by prefix.
        # BGP dynamics count from beginning to end. IPv4 variables
        self.wadi = 0
        self.aadi = 0
        self.wwdu = 0
        self.aadut1 = 0
        self.aadut2 = 0
        self.wadu = 0
        self.aw = 0

    def add(self, update):
        utime = update.get_time()
        if self.start = 0:# first run
            self.start = utime
            self.end = utime
        else:# Not first run
            if update.get_dynamic_type() == 'A':
                upfx_list = update.get_announce() 
            elif update.get_dynamic_type() == 'W':
                upfx_list = update.get_withdrawn()
            else:# We currently do not deal with other types
                return 0
            if self.end == utime:# No need to move window forward
                for upfx in upfx_list:
                    find_pfx = self.trie4.key(upfx, start = 0, end = None, default = None)
                    if find_pfx == None or len(find_pfx) != len(upfx):# No corresponding prefix stored
                        self.trie4[upfx] = []# Add new node value: a list of updates
                        self.trie4[upfx].append(update)# Add this update as first one
                    else:# Prefix has been stored before
                        update_list = self.trie4[upfx]
                        for ud in reversed(update_list):
                            if ud.
                    #If not: add this node
                    #If yes: variable + 1
            elif self.end < utime:
                if self.size < self.maxsize:# Just increase window end
                    self.size += utime - self.end
                    self.end = utime
                    if self.size > self.maxsize: # When utime - end > 1
                        # TODO:delete outside updates
                else:
                    self.start += utime - self.end
                    self.end = utime
                    # TODO:delete outside updates

            else:
                print 'Wrong!'
        elif self.size < self.maxsize:
        elif self.size == self.maxsize:
            time = update.get_time()
            if time > ctime:
                # move forward
        if self.size < self.maxsize:
            self.end += 1
        if self.size == self.maxsize:
            self.start += 1
            self.end += 1
            # TODO: delete the smallest key and value

        self.update_dict[self.end] = []
        for line in ...# TODO: fulfil the new list by updates
            #Create update objects and store them in dict
            # check time and ip, if not interested, do not create obj

    def analyze():
        # anylize new updates and add variables
