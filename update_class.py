from datetime import datetime
from netaddr import *

class Update():
    def __init__(self, string):
        # initialize self values
        self.next_hop = None
        self.announce = []
        self.withdrawn = []
        self.as_path = None 
        self.communities = None
        self.origin = None

        string = string.split('\n')
        for line in string:
            if line == '' or line == '\n':# may occur at beginning or end
                continue
            line.replace('|', '') # IPv6 updates has '|' in them
            header = line.split(': ')[0]
            try:
                content = line.split(': ')[1]
            except:
                continue
            
            if header == 'TIME':
                dt = datetime.strptime(content, '%Y-%m-%d %H:%M:%S') 
                self.time = time.mktime(dt.timetuple())# Datetime in seconds
            elif header == 'FROM':
                addr = IPAddress(content).bits()
                # Address format modification
                if len(addr) > 100:# IPv6 addr
                    self.from_ip = addr.replace(':', '')
                    self.protocol = 6
                else:# IPv4 addr
                    self.from_ip = addr.replace('.', '')
                    self.protocol = 4

                # If this is from our interested BGP peer IP
                if addr in self.addr4_list or addr in self.addr6_list:
                    if dt_gra not in self.update_count.keys():
                        self.update_count[dt_gra] = [0, 0]
                    if addr in self.addr4_list:# if it is our interesting
                        # BGP peer v4 address 
                        self.update_count[dt_gra][0] += 1
                    elif addr in self.addr6_list:# if it is our interesting
                        # BGP peer v6 address 
                        self.update_count[dt_gra][1] += 1
            elif header == 'NEXT_HOP':
                self.next_hop =
            elif header == 'ANNOUNCE':
                self.announce.append(self.pfx_to_binary())
            elif header == 'WITHDRAWN':
                self.withdrawn.append(self.pfx_to_binary())
            elif header == 'AS_PATH':
                self.as_path = # a list
            elif header == 'COMMUNITIES':
                self.communities =
            elif header == 'ORIGIN':
                self.origin =
            else:
                print header
                pass

    def pfx_to_binary(self, content):
        

    def equal_to(self, Update u):
        # May be incomplete.
        if self.next_hop == u.next_hop and self.as_path == u.as_path and
        self.communities ==u.communities and self.origin = u.origin:
            return True
        else:
            return False

    def get_time(self):
        return self.time

    def get_from_ip(self):
        return self.from_ip

    def get_announce(self):# 0 1 string
        return self.announce

    def get_withdrawn(self):# 0 1 string
        return self.withdrawn

    def get_dynamic_type(self):# Withdraw & Announce & Other
        if self.announce != [] and self.withdrawn == []:
            return 'A'
        elif self.announce == [] and self.withdrawn != []:
            return 'W'
        else:
            return 'O'
