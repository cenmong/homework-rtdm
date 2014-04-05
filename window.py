class Window():
    def __init__(self, maxsize, time_start):
        self.size = 0
        self.maxsize = maxsize
        self.update_dict4 = {} # time in seconds: list of update obj
        self.update_dict6 = {} 
        self.start = time_start# Window start
        self.end = time_start# Window end
        # BGP dynamics count from beginning to end
        # IPv4 variables
        self.wadi4 = 0
        self.aadi4 = 0
        self.wwdu4 = 0
        self.aadu4t1 = 0
        self.aadu4t2 = 0
        self.wadu4 = 0
        self.aw4 = 0
        # IPv6 variables
        self.wadi6 = 0
        self.aadi6 = 0
        self.wwdu6 = 0
        self.aadu6t1 = 0
        self.aadu6t2 = 0
        self.wadu6 = 0
        self.aw6 = 0

    def move_forward(self, ):# TODO: add file name which has correct pointer
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
