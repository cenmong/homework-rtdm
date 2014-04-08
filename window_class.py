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

    def add(self, update):
        utime = update.get_time()
        if self.start == 0:# first run
            self.start = utime
            self.end = utime
            self.size = 1
        else:# Not first run
            if self.end < utime:
                if self.size < self.maxsize: #increase window
                    self.size += utime - self.end
                    self.end = utime
                    if self.size > self.maxsize: # When utime - end > 1, may not happen
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
        self.analyze_updates(update)

    def analyze_updates(self, update):
        a_list = [] # Announced prefix list
        w_list = [] # Withdrawn prefix list
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
                has_change = False
                update_list = self.trie.value(upfx, start=0, end=None)
                for ud in reversed(update_list): # Latest first
                    if upfx in ud.get_announce() and ud.equal_to(update):
                        self.aadut1 += 1
                        has_change = True
                        break
                    elif upfx in ud.get_announce() and not\
                    ud.equal_to(update) and ud.as_path == update.as_path and\
                    ud.next_hop == update.next_hop:
                        self.aadut2 += 1
                        has_change = True
                        break
                    elif upfx in ud.get_withdrawn() and not\
                    ud.equal_to(update):
                        self.wadi += 1
                        has_change = True
                        break
                    elif upfx in ud.get_announce() and not\
                    ud.equal_to(update):
                        self.aadi += 1
                        has_change = True
                        break
                    elif upfx in ud.get_withdrawn() and\
                    ud.has_same_path(update):
                        self.wadu += 1
                        has_change = True
                        break

                if has_change:
                    update_list.remove(ud)
                else:
                    pass
                update_list.append(update)
                self.trie[upfx] = update_list

        for upfx in w_list:
            find_pfx = self.trie.key(upfx, start=0, end=None, default=None)

            if self.trie.value(find_pfx, start=0, end=None) == None or find_pfx\
            == None or len(find_pfx) != len(upfx):# No corresponding prefix
                                                  #  (excluding root) stored
                self.trie[upfx] = []# a list of updates
                self.trie[upfx].append(update)# Add this update as first one
            else:# Prefix has been stored
                has_change = False
                update_list = self.trie.value(upfx, start=0, end=None)
                for ud in reversed(update_list): # Latest first
                    if upfx in ud.get_withdrawn() and\
                    ud.equal_to(update):
                        self.wwdu += 1
                        has_change = True
                        break
                    elif upfx in ud.get_announce() and\
                    ud.has_same_path(update):
                        self.aw += 1
                        has_change = True
                        break

                if has_change:
                    update_list.remove(ud)
                else:
                    pass
                update_list.append(update)
                self.trie[upfx] = update_list
        return 0

    def cut_trie(self):
        for ulist in sorted(self.trie):
            try:
                for update in ulist:
                    if update.get_time() < self.start:
                        ulist.remove(update)
                if ulist == []:
                    del ulist # Not sure this node does not exist any more!!!
            except:
                pass
