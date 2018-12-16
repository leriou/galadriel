#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mul
from multiprocessing import Pool
import os, time, random

class TaskManager:

    def __init__(self):
        self.sum_res = 0
        self.loop = True

    def spfib(self, n, a, b):  # simple fib
        if n <= 0:
            return a
        return self.spfib(n - 1, b, a + b)
        
    @staticmethod
    def long_time_task(self,name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(4)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    
    def multi_proccess(self):
        print('Parent process %s.' % os.getpid())
        p = Pool(2)
        for i in range(5):
            p.apply_async(TaskManager.long_time_task,args=(self,i))
            
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')

    def run(self):
        # self.multi_proccess()
        self.use_queue()

    def use_queue(self):
        queue = mul.JoinableQueue()
        for c in range(1, 100, 2):
            self.add_to_queue(c, c + 1, queue)
        while self.loop:
            if queue.get(True) > 90:
                self.loop = False
        print("result->", self.sum_res)

    def add_to_queue(self, a, b, q):
        self.add(a, b)
        q.put(a)

    def add(self, a, b):
        self.sum_res = a + b + self.sum_res
        return a + b


if __name__ == '__main__':
    tm = TaskManager()
    tm.run()
