from update_class import *
from netaddr import *
import patricia

class Window():

    def __init__(self, maxsize):
        # Window parameters
        self.maxsize = maxsize
        self.size = 0
        self.start = 0  # Window start
        self.end = 0  # Window end
        self.trie = patricia.trie(None)  # Store still active updates.
        # BGP dynamics count variables
        self.wadi = 0
        self.aadi = 0
        self.wwdu = 0
        self.aadut1 = 0
        self.aadut2 = 0
        self.wadu = 0
        self.aw = 0
        #self.time_update = {}

    def add(self, update):
        if update.is_abnormal():
            print '!!!!!!!!!!!!'
            return 0
        utime = update.get_time()
        if self.start == 0:  # first run
            self.start = utime
            self.end = utime
            self.size = 1
        else:
            if self.end < utime:
                if self.size < self.maxsize:  # increase window
                    self.size += utime - self.end
                    self.end = utime
                    if self.size > self.maxsize:  # When utime - end > 1
                        self.start += self.size - self.maxsize
                        self.size = self.maxsize
                        #self.cut_trie()  # Delete outside updates
                else:  # size alraedy maximum
                    self.start += utime - self.end
                    self.end = utime
                    #self.cut_trie()
            elif self.end > utime:
                print 'Wrong update time!'
            else:
                pass
        #try:
        #    self.time_update[utime].append(update)
        #except:
        #    self.time_update[utime] = []
        self.analyze_update(update)

        return 0

    def analyze_update(self, update):
        a_list = update.get_announce() 
        w_list = update.get_withdrawn()

        for upfx in a_list:
            try:
                update_list = self.trie[upfx]
            except:
                self.trie[upfx] = []
                self.trie[upfx].append(update)
                continue

            change = False
            for ud in reversed(update_list): # Latest first
                if ud.get_time() < self.start:
                    update_list.remove(ud)
                    continue

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
                    if ud.has_same_path(update):
                        self.wadu += 1
                    else:
                        self.wadi += 1
                    change = True
                    break
                else:  # Normally, this will not happen.
                    update_list.remove(ud)
                    continue

            if change:
                update_list.remove(ud)

            if update not in update_list:  # Normally, this will be True.
                update_list.append(update)

            self.trie[upfx] = update_list

        for upfx in w_list:
            try:
                update_list = self.trie[upfx]
            except:
                self.trie[upfx] = []
                self.trie[upfx].append(update)
                continue

            change = False
            for ud in reversed(update_list):
                if ud.get_time() < self.start:
                    update_list.remove(ud)
                    continue

                if upfx in ud.get_withdrawn():
                    self.wwdu += 1
                    change = True
                    break
                elif upfx in ud.get_announce() and ud.has_same_path(update):
                    self.aw += 1
                    change = True
                    break
                else:
                    update_list.remove(ud)
                    continue

            if change:
                update_list.remove(ud)

            if update not in update_list:
                update_list.append(update)

            self.trie[upfx] = update_list

        return 0

    def cut_trie(self):  # Delete updates that are out of current window.
        print 'trie size before cut = ', len(self.trie)
        for addr in sorted(self.trie):
            ulist = self.trie[addr]
            try:
                for update in ulist:
                    if update.get_time() < self.start:
                        ulist.remove(update)
                if ulist == []:
                    del self.trie[addr]
            except:  # root node has value None
                pass
        print 'trie size after cut = ', len(self.trie)
        return 0
