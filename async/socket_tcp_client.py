#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
# print(s.recv(1024).decode('utf-8'))
for data in [b'ping',b'push msg mt1',b'push msg ac1', b'push msg ac5', b'set msg1 1',b'pop msg',b'pop msg']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
