from update_class import *
from netaddr import *
import patricia

class Window():

    def __init__(self, maxsize):
        # Window parameters
        self.maxsize = maxsize
        self.size = 0
        self.start = 0# Window start
        self.end = 0# Window end
        self.trie = patricia.trie(None) #Store still active updates.
        # BGP dynamics count variables
        self.wadi = 0
        self.aadi = 0
        self.wwdu = 0
        self.aadut1 = 0
        self.aadut2 = 0
        self.wadu = 0
        self.aw = 0
        self.time_update = {}

    def add(self, update):
        if update.is_abnormal():
            print '!!!!!!!!!!!!'
            return 0
        utime = update.get_time()
        if self.start == 0:# first run
            self.start = utime
            self.end = utime
            self.size = 1
        else:
            if self.end < utime:
                if self.size < self.maxsize: #increase window
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
            elif self.end > utime:
                print 'Wrong update time!'
            else:
                pass
        try:
            self.time_update[utime].append(update)
        except:
            self.time_update[utime] = []
        self.analyze_updates(update)

    def analyze_updates(self, update):
        a_list = update.get_announce() 
        w_list = update.get_withdrawn()

        for upfx in a_list:
            find_pfx = self.trie.key(upfx, start=0, end=None, default=None)

            if self.trie.value(find_pfx, start=0, end=None) == None or find_pfx\
            == None or len(find_pfx) != len(upfx):# No corresponding prefix
                                                  #  (excluding root) stored
                self.trie[upfx] = []# a list of updates
                self.trie[upfx].append(update)# Add this update as first one
            else:# Prefix has been stored
                change = False
                update_list = self.trie.value(upfx, start=0, end=None)
                for ud in reversed(update_list): # Latest first
                    if upfx in ud.get_announce():
                        if ud.equal_to(update):
                            self.aadut1 += 1
                        else:
                            if ud.as_path == update.as_path and\
                            ud.next_hop == update.next_hop:
                                self.aadut2 += 1
                            else:
                                self.aadi += 1
                        change = True
                        break
                    elif upfx in ud.get_withdrawn():
                        if not ud.equal_to(update):
                            if ud.has_same_path(update):
                                self.wadu += 1
                            else:
                                self.wadi += 1
                        else:
                                self.wadu += 1
                        change = True
                        break
                    else:
                         continue

                if change:
                    update_list.remove(ud)

                if update not in update_list: # A new update may cause many hits
                    update_list.append(update)

                self.trie[upfx] = update_list

        for upfx in w_list:
            find_pfx = self.trie.key(upfx, start=0, end=None, default=None)

            if self.trie.value(find_pfx, start=0, end=None) == None or find_pfx\
            == None or len(find_pfx) != len(upfx):
                self.trie[upfx] = []
                self.trie[upfx].append(update)
            else:
                change = False
                update_list = self.trie.value(upfx, start=0, end=None)
                for ud in reversed(update_list):
                    if upfx in ud.get_withdrawn()\
                        and ud.equal_to(update):
                            self.wwdu += 1
                            change = True
                            break
                    elif upfx in ud.get_announce()\
                        and ud.has_same_path(update):
                            self.aw += 1
                            change = True
                            break
                    else:
                        continue

                if change:
                    update_list.remove(ud)

                if update not in update_list:
                    update_list.append(update)

                self.trie[upfx] = update_list

        return 0

    def cut_trie(self):
        for t in self.time_update.keys():
            if t < self.start:
                for u in self.time_update[t]:
                    del u
                del self.time_update[t]
        '''
        for ulist in sorted(self.trie):
            try:
                for update in ulist:
                    if update.get_time() < self.start:
                        ulist.remove(update)
                if ulist == []:
                    del ulist
            except:
                pass'''
