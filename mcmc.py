# -*- coding: utf-8 -*-

from random import randint
from random import random

class MCMC:
    def __init__(self, fx):
        self.__fx = fx
        self.__len = len(fx)
        self.sample = [0] * self.__len
        self.x = randint(0, self.__len - 1)
    
    def sampling(self, loop_count = 1):
        for i in range(loop_count):
            d = randint(0, 1) * 2 - 1 # -1 or 1
            r = random()
            t = (self.x + d + self.__len) % self.__len
            fx = self.__fx[self.x]
            ft = self.__fx[t]
            if (fx == 0 or fx < ft or ft / fx > r):
                self.x = t
            
            self.sample[self.x] = self.sample[self.x] + 1
    
    def printSample(self):
        for i, n in enumerate(self.sample):
            print("{0}:{1}".format(i, n))
        
    def fx(self, x):
        return self.__fx[x]

class ReplicaExchange:
    def __init__(self, mcmc_list):
        self.__mcmc_list = mcmc_list;
    
    def exchange(mcmc_a, mcmc_b):
        # 変更前
        ax = mcmc_a.x
        bx = mcmc_b.x
        a_fx_a = mcmc_a.fx(ax)
        b_fx_b = mcmc_b.fx(bx)
        # 変更後
        a_fx_b = mcmc_a.fx(bx)
        b_fx_a = mcmc_b.fx(ax)
        
        if (a_fx_a * b_fx_b == 0):
            return
        
        r = random()
        if ((a_fx_b * b_fx_a) / (a_fx_a * b_fx_b) > r):
            mcmc_a.x = bx
            mcmc_b.x = ax
        
    def sampling(self, mcmc_loop_count, re_loop_count):
        start = 0
        for i in range(re_loop_count):
            for mcmc in self.__mcmc_list:
                mcmc.sampling(mcmc_loop_count)
            for j in range(start, len(self.__mcmc_list) - 1, 2):
                ReplicaExchange.exchange(self.__mcmc_list[j], self.__mcmc_list[j + 1])
            start = (start + 1) % 2
    
    def printSample(self):
        for i, mcmc in enumerate(self.__mcmc_list):
            print("-----{0}-----".format(i))
            mcmc.printSample()

#f = MCMC([1,2,3,4,4,3,2,1])
#f.sampling(20000)
#f.printSample()

mcmc_list = [
        MCMC([2,3,4,5,6,7,8,0]),
        MCMC([2,3,4,0,6,7,8,0]),
        MCMC([2,3,0,0,0,7,8,0])
        ]

#mcmc_list = [
#        MCMC([1,1,1,1,1,1,1,0]),
#        MCMC([2,2,2,0,3,3,3,0]),
#        MCMC([2,3,0,0,0,7,8,0])
#        ]

replica = ReplicaExchange(mcmc_list)
replica.sampling(100, 2000)
replica.printSample()
