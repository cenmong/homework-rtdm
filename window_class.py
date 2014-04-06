from update_class import *
from netaddr import *
import patricia

class Window():
    def __init__(self, maxsize, protocol_type):
        self.ptype = protocol_type
        # Window parameters
        self.maxsize = maxsize
        self.size = 0
        self.start = 0# Window start
        self.end = 0# Window end
        self.trie = patricia.trie(None)# Store still active updates by prefix.
        # BGP dynamics count variables
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
                   
            if self.end == utime:# No need to tackle window size
                self.analyze_updates(upfx_list)
            elif self.end < utime:
                if self.size < self.maxsize:# Just increase window end
                    self.size += utime - self.end
                    self.end = utime
                    if self.size > self.maxsize: # When utime - end > 1
                        self.start += self.size - self.maxsize
                        self.size = self.maxsize
                        self.cut_trie()# Delete outside updates
                else:# size alraedy maximum
                    self.start += utime - self.end
                    self.end = utime
                    self.cut_trie()
            else:# end > utime
                print 'Wrong!'

    def analyze_updates(self, update_list)
        for upfx in update_list:
            find_pfx = self.trie4.key(upfx, start = 0, end = None, default = None)
            if find_pfx == None or len(find_pfx) != len(upfx):# No corresponding prefix stored
                self.trie4[upfx] = []# Add new node value: a list of updates
                self.trie4[upfx].append(update)# Add this update as first one
            else:# Prefix has been stored before
                update_list = self.trie4[upfx]
                for ud in reversed(update_list):
                    if ud.get_dynamic_type() == 'A' and\
                    update.get_dynamic_type() == 'A' and\
                    ud.equal_to(update):
                        self.aadut1 += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue
                    if ud.get_dynamic_type() == 'A' and\
                    update.get_dynamic_type() == 'A' and not\
                    ud.equal_to(update) and ...:
                        self.aadut2 += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue
                    if ud.get_dynamic_type() == 'W' and\
                    update.get_dynamic_type() == 'A' and not\
                    ud.equal_to(update):
                        self.wadi += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue
                    if ud.get_dynamic_type() == 'A' and\
                    update.get_dynamic_type() == 'A' and not\
                    ud.equal_to(update):
                        self.aadi += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue
                    if ud.get_dynamic_type() == 'W' and\
                    update.get_dynamic_type() == 'W' and\
                    ud.equal_to(update):
                        self.wwdu += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue
                    if ud.get_dynamic_type() == 'W' and\
                    update.get_dynamic_type() == 'A' and not\
                    ud.equal_to(update) and ud.has_same_path(update):
                        self.wadu += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue
                    if ud.get_dynamic_type() == 'A' and\
                    update.get_dynamic_type() == 'W' and not\
                    ud.equal_to(update) and ud.has_same_path(update):
                        self.aw += 1
                        update_list.remove(ud)
                        update_list.append(update)
                        continue

    def cut_trie(self):
        for ulist in sorted(self.trie):
            try:
                for update in ulist:
                    if update.get_time() < self.start:
                        ulist.remove(update)
                if ulist == []:
                    del ulist
            except:
                pass
