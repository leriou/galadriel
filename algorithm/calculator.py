#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import time


class Calculator:

    def __init__(self):
        self.num = 10
        self.a = 1
        self.res = 0

    def getPi(self):
        for n in range(1, self.num):
            m = 1 / (1 + 2 * n)
            if n % 2 == 0:
                self.a = self.a + m
            else:
                self.a = self.a - m
        return self.a * 4

    def getE(self):
        for n in range(0, self.num):
            self.res = self.res + 1 / math.factorial(n)
        return self.res

    def getAge(self):
        now = time.time()
        born_stmp = time.mktime((1993, 1, 29, 23, 0, 0, 0, 0, 0))
        age = (now - born_stmp) / (365 * 24 * 3600)
        return age


if __name__ == "__main__":
    c = Calculator()
    print("age: %f " % c.getAge())
    print("e为: %f " % c.getE())
    print("pi等于: %f " % c.getPi())
