#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('10.113.1.231',7001))


def rstp(s):
    res = []
    res.append("*"+str(len(s.split())))
    for n in s.split():
        res.append("$"+str(len(n)))
        res.append(n)
    return bytes("\r\n".join(res)+"\r\n",encoding="utf8")

for data in ["set a 190","expire a 40","cluster info","cluster nodes","hgetall ads:place:6"]:
    s.send(rstp(data))
    print(rstp(data))
    print(s.recv(4096).decode('utf-8'))
    # time.sleep(1)
s.close()