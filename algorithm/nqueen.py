#! /usr/bin/env python
# -*- coding: utf-8 -*-

import fire


class Nqueen:

    def __init__(self, n):
        self.n = n
        self.count = 0
        self.map = []
        for i in range(0, self.n):
            self.map.append(0)

    def main(self):
        self.run(0)
        print("总共%d种方案" % self.count)

    def run(self, index):
        loop = 0
        for loop in range(0, self.n):
            if self.check(index, loop):
                self.map[index] = loop
                if self.n - 1 == index:
                    self.count += 1
                    self.echo()
                    return
                else:
                    self.run(index + 1)

    def echo(self):
        for i in range(0, self.n):
            inner = 0
            str = ''
            for inner in range(0, self.n):
                if inner == self.map[i]:
                    str += "1 "
                else:
                    str += "0 "
            print(str)
        print("=======================")

    def check(self, loop, value):
        for index in range(0, loop):
            data = self.map[index]
            if value == data:
                return 0
            if ((index + data) == (loop + value)):
                return 0
            if ((index - data) == (loop - value)):
                return 0
        return 1


if __name__ == "__main__":
    # python3 nqueen main
    fire.Fire(Nqueen(8))
