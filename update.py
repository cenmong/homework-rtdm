class Update():
    def __init__(self, string):
        # initialize self values
        self.next_hop = None
        self.announce = None
        self.as_path = None 
        self.communities = None
        self.origin = None

        string = string.split('\n')
        for line in string:
            if line == '':# may occur at beginning or end
                continue
            line.replace('|', '') # IPv6 updates has '|' in them
            header = line.split(': ')[0]
            try:
                content = line.split(': ')[1]
            except:
                continue
            
            if header == 'TIME':
                self.time =
            elif header == 'FROM':
                self.from_ip =
                self.protocol = # 4 or 6
            elif header == 'NEXT_HOP':
                self.next_hop =
            elif header == 'ANNOUNCE':
                self.announce = 
            elif header == 'AS_PATH':
                self.as_path = # a list
            elif header == 'COMMUNITIES':
                self.communities =
            elif header == 'ORIGIN':
                self.origin =
            else:
                print header
                pass

    def equal_to (self, Update u):
        if self.next_hop == u.next_hop and self.announce == u.announce and ...:
            return True
        else:
            return False

        
