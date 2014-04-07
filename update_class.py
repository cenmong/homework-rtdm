from datetime import datetime
from netaddr import *
import time

class Update():

    def __init__(self, string):
        self.next_hop = None
        self.announce = []
        self.withdrawn = []
        self.as_path = []
        self.communities = None
        self.origin = None
        self.protocol = None# For modifing prefix format

        string = string.split('@@@')
        for line in string:
            if string == '':# May exist at the end
                continue
            line.replace('|', '') # IPv6 updates has '|'

            header = line.split(': ')[0]
            try:
                content = line.split(': ')[1]
            except:
                continue
            
            if header == 'TIME':
                dt = datetime.strptime(content, '%Y-%m-%d %H:%M:%S') 
                self.time = time.mktime(dt.timetuple())# Datetime in seconds
                print self.time # For debug
            elif header == 'FROM':
                addr = IPAddress(content).bits()
                if len(addr) > 100:# IPv6 addr
                    self.from_ip = addr.replace(':', '')
                    self.protocol = 6
                else:
                    self.from_ip = addr.replace('.', '')
                    self.protocol = 4 

            elif header == 'NEXT_HOP':
                self.next_hop = self.pfx_to_binary(content)
            elif header == 'ANNOUNCE':
                self.announce.append(self.pfx_to_binary(content))
            elif header == 'WITHDRAWN':
                self.withdrawn.append(self.pfx_to_binary(content))
            elif header == 'AS_PATH':
                self.as_path = content.split()
            elif header == 'COMMUNITIES':
                self.communities = content# Store string really OK?
            elif header == 'ORIGIN':
                self.origin = content
            else:
                print 'unrecognized header: ', header
                pass

    def pfx_to_binary(self, content):
        if self.protocol == 4:
            addr = IPAddress(content).bits()
            addr = addr.replace('.', '')
            return addr
        elif self.protocol == 6:
            addr = IPAddress(content).bits()
            addr = addr.replace(':', '')
            return addr
        else:
            print 'protocol false!'
            return 0

    def equal_to(self, Update u):# According to Jun Li, do not consider prefix
        # May be incomplete.
        if self.next_hop == u.next_hop and self.as_path == u.as_path and
        self.communities ==u.communities and self.origin = u.origin:
            return True
        else:
            return False

    def has_same_path(self, Update u):
        if self.as_path == u.as_path:
            return True
        else:
            return False

    def get_time(self):
        return self.time

    def get_from_ip(self):
        return self.from_ip

    def get_announce(self):
        return self.announce

    def get_withdrawn(self):
        return self.withdrawn

    def get_dynamic_type(self):# Withdraw & Announce & Other
        if self.announce != [] and self.withdrawn == []:
            return 'A'
        elif self.announce == [] and self.withdrawn != []:
            return 'W'
        elif self.announce != [] and self.withdrawn != []:
            print 'type error!'
        else:
            return 'O'
