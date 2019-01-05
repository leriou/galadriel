#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys 
sys.path.append("..") 
from tools import di
import random
import time

'''
基于Bitmap算法的会员标签匹配

支持的操作:

1. 判断某用户是否含有某一或多个标签
2. 获取某个标签下面的所有用户

存储方案:

1. 基于redis的string类型, 使用setbit操作以节省存储空间

示例:

user:vip: 010101010000110

类似以上表示 用户ID为 1,3,5,7,12,13的用户是vip会员(相应位置的比特位为1)

'''


class Bitmap:

    def __init__(self):
        self.di = di.Di()
        self.redis = self.di.getRedis()
        self.mongo = self.di.getMongoDb()
        self._init_bittable()
        self.key_map = [
            "user:all",
            "user:member",
            "user:vip",
            "user:mobile",
            "user:mac",
            "user:supervip",
            "user:gender_female",
            "user:gender_male",
            "user:email"
        ]

    def get_random(self):
        return (int)(random.random() < 0.499999)

    def init_db(self, n):
        db = self.mongo["bitmap"]["user"]
        uid = 1
        user_list = []
        pipe = self.redis.pipeline()
        for i in range(1, n):
            data = {
                "uid": i,
                "name":"user_" + str(i),
                "isMember": self.get_random(),  # 是否会员
                "isVip": self.get_random(),  # 是否vip
                "gender": self.get_random(),  # 性别
                "isMobile": self.get_random(),  # 是否程序员
                "isEmail": self.get_random(),  # 是否说唱歌手
                "isMac": self.get_random(),
                "isSupervip": self.get_random()
            }
            user_list.append(data)
            pipe.setbit("user:all", i, data['uid'])
            pipe.setbit("user:member", i, data['isMember'])
            pipe.setbit("user:vip", i, data['isVip'])
            pipe.setbit("user:mobile", i, data['isMobile'])
            pipe.setbit("user:mac", i, data['isMac'])
            pipe.setbit("user:supervip", i, data['isSupervip'])
            pipe.setbit("user:email", i , data["isEmail"] )
            if data['gender'] == 1:
                gender_key = "user:gender_female"
            else:
                gender_key = "user:gender_male"
            pipe.setbit(gender_key, i, 1)
            if i % 1000 == 0:
                print(i)
        pipe.execute()
        db.insert_many(user_list)

    def _init_bittable(self):
        self.bit_table = [[], [8], [7], [7, 8], [6], [6, 8], [6, 7], [6, 7, 8], [5], [5, 8], [5, 7],[5, 7, 8], [5, 6], [5, 6, 8], [5, 6, 7], [5, 6, 7, 8], [4], [4, 8], [4, 7], [4, 7, 8],[4, 6], [4, 6, 8], [4, 6, 7], [4, 6, 7, 8], [4, 5], [4, 5, 8], [4, 5, 7], [4, 5, 7, 8], [4, 5, 6],[4, 5, 6, 8], [4, 5, 6, 7], [4, 5, 6, 7, 8], [3], [3,8], [3, 7],[3, 7, 8], [3, 6], [3, 6, 8], [3, 6, 7], [
                              3, 6, 7, 8], [3, 5], [3, 5, 8], [3, 5, 7],
                          [3, 5, 7, 8], [3, 5, 6], [3, 5, 6, 8], [
                              3, 5, 6, 7], [3, 5, 6, 7, 8], [3, 4],
                          [3, 4, 8], [3, 4, 7], [3, 4, 7, 8], [3, 4, 6], [
                              3, 4, 6, 8], [3, 4, 6, 7], [3, 4, 6, 7, 8],
                          [3, 4, 5], [3, 4, 5, 8], [3, 4, 5, 7], [
                              3, 4, 5, 7, 8], [3, 4, 5, 6], [3, 4, 5, 6, 8],
                          [3, 4, 5, 6, 7], [3, 4, 5, 6, 7, 8], [
                              2], [2, 8], [2, 7], [2, 7, 8], [2, 6],
                          [2, 6, 8], [2, 6, 7], [2, 6, 7, 8], [2, 5], [
                              2, 5, 8], [2, 5, 7], [2, 5, 7, 8],
                          [2, 5, 6], [2, 5, 6, 8], [2, 5, 6, 7], [
                              2, 5, 6, 7, 8], [2, 4], [2, 4, 8], [2, 4, 7],
                          [2, 4, 7, 8], [2, 4, 6], [2, 4, 6, 8], [
                              2, 4, 6, 7], [2, 4, 6, 7, 8], [2, 4, 5],
                          [2, 4, 5, 8], [2, 4, 5, 7], [2, 4, 5, 7, 8], [2, 4, 5, 6], [2, 4, 5, 6, 8],
                          [2, 4, 5, 6, 7], [2, 4, 5, 6, 7, 8], [
                              2, 3], [2, 3, 8], [2, 3, 7], [2, 3, 7, 8],
                          [2, 3, 6], [2, 3, 6, 8], [2, 3, 6, 7], [
                              2, 3, 6, 7, 8], [2, 3, 5], [2, 3, 5, 8],
                          [2, 3, 5, 7], [2, 3, 5, 7, 8], [2, 3, 5, 6], [
                              2, 3, 5, 6, 8], [2, 3, 5, 6, 7],
                          [2, 3, 5, 6, 7, 8], [2, 3, 4], [2, 3, 4, 8], [2, 3, 4, 7], [2, 3, 4, 7, 8],
                          [2, 3, 4, 6], [2, 3, 4, 6, 8], [2, 3, 4, 6, 7], [
                              2, 3, 4, 6, 7, 8], [2, 3, 4, 5],
                          [2, 3, 4, 5, 8], [2, 3, 4, 5, 7], [2, 3, 4, 5, 7, 8], [
                              2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 8],
                          [2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 8], [1], [
                              1, 8], [1, 7], [1, 7, 8], [1, 6], [1, 6, 8],
                          [1, 6, 7], [1, 6, 7, 8], [1, 5], [1, 5, 8], [
                              1, 5, 7], [1, 5, 7, 8], [1, 5, 6], [1, 5, 6, 8],
                          [1, 5, 6, 7], [1, 5, 6, 7, 8], [1, 4], [1, 4, 8], [1, 4, 7], [
                              1, 4, 7, 8], [1, 4, 6], [1, 4, 6, 8], [1, 4, 6, 7],
                          [1, 4, 6, 7, 8], [1, 4, 5], [1, 4, 5, 8], [1, 4, 5, 7], [1, 4, 5, 7, 8],
                          [1, 4, 5, 6], [1, 4, 5, 6, 8], [1, 4, 5, 6, 7], [1, 4, 5, 6, 7, 8], [1, 3],
                          [1, 3, 8], [1, 3, 7], [1, 3, 7, 8], [1, 3, 6], [1, 3, 6, 8], [1, 3, 6, 7],
                          [1, 3, 6, 7, 8], [1, 3, 5], [1, 3, 5, 8], [
                              1, 3, 5, 7], [1, 3, 5, 7, 8], [1, 3, 5, 6],
                          [1, 3, 5, 6, 8], [1, 3, 5, 6, 7], [1, 3, 5, 6, 7, 8], [
                              1, 3, 4], [1, 3, 4, 8], [1, 3, 4, 7],
                          [1, 3, 4, 7, 8], [1, 3, 4, 6], [1, 3, 4, 6, 8], [
            1, 3, 4, 6, 7], [1, 3, 4, 6, 7, 8], [1, 3, 4, 5],
            [1, 3, 4, 5, 8], [1, 3, 4, 5, 7], [1, 3, 4, 5, 7, 8], [1, 3, 4, 5, 6], [1, 3, 4, 5, 6, 8],
            [1, 3, 4, 5, 6, 7], [1, 3, 4, 5, 6, 7, 8], [1, 2], [
                1, 2, 8], [1, 2, 7], [1, 2, 7, 8], [1, 2, 6],
            [1, 2, 6, 8], [1, 2, 6, 7], [1, 2, 6, 7, 8], [1, 2, 5], [
                1, 2, 5, 8], [1, 2, 5, 7], [1, 2, 5, 7, 8],
            [1, 2, 5, 6], [1, 2, 5, 6, 8], [1, 2, 5, 6, 7], [
                1, 2, 5, 6, 7, 8], [1, 2, 4], [1, 2, 4, 8], [1, 2, 4, 7],
            [1, 2, 4, 7, 8], [1, 2, 4, 6], [1, 2, 4, 6, 8], [
                1, 2, 4, 6, 7], [1, 2, 4, 6, 7, 8], [1, 2, 4, 5],
            [1, 2, 4, 5, 8], [1, 2, 4, 5, 7], [1, 2, 4, 5, 7, 8], [1, 2, 4, 5, 6], [1, 2, 4, 5, 6, 8],
            [1, 2, 4, 5, 6, 7], [1, 2, 4, 5, 6, 7, 8], [1, 2, 3], [
                1, 2, 3, 8], [1, 2, 3, 7], [1, 2, 3, 7, 8],
            [1, 2, 3, 6], [1, 2, 3, 6, 8], [1, 2, 3, 6, 7], [
                1, 2, 3, 6, 7, 8], [1, 2, 3, 5], [1, 2, 3, 5, 8],
            [1, 2, 3, 5, 7], [1, 2, 3, 5, 7, 8], [1, 2, 3, 5, 6], [
                1, 2, 3, 5, 6, 8], [1, 2, 3, 5, 6, 7],
            [1, 2, 3, 5, 6, 7, 8], [1, 2, 3, 4], [1, 2, 3, 4, 8], [1, 2, 3, 4, 7], [1, 2, 3, 4, 7, 8],
            [1, 2, 3, 4, 6], [1, 2, 3, 4, 6, 8], [1, 2, 3, 4, 6, 7], [
                1, 2, 3, 4, 6, 7, 8], [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5, 8], [1, 2, 3, 4, 5, 7], [1, 2, 3, 4, 5, 7, 8], [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6, 8], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8]]

    def build_bit_table(self):  # 生成0-255的表
        arr = []
        for i in range(0, 256):
            tmp_arr = []
            tstr = bin(i).replace('0b', '').zfill(8)
            n = 0
            for k in tstr:
                n = n + 1
                if int(k) == 1:
                    tmp_arr.append(n)
            arr.append(tmp_arr)
        self.bit_table = arr

    def get(self, key):  # 获取redis某key的值
        return self.redis.get(key)

    def key2array(self, key):  # 将二进制('\x05'->'0b00000101')变为数组[5,7], 表示第五位和第七位为1
        tmpstr = ''.join([bin(i).replace('0b', '').zfill(8) for i in key])
        arr = []
        str_len = len(tmpstr)
        for i in range(0, str_len):
            if int(tmpstr[i]) == 1:
                arr.append(i)
        return (arr)

    def key2array2(self, key):
        arr = []
        n = 0  # 每次循环的最低数字
        for i in key:
            k = 0
            if i > 0:
                for p in bin(i).replace('0b', '').zfill(8):
                    k = k + 1
                    if int(p) == 1:
                        arr.append(n + k - 1)
            n = n + 8
        return (arr)

    def key2array3(self, key):  # 查表法
        arr = []
        n = 0
        for i in key:
            pos = self.bit_table[i]
            for k in pos:
                arr.append(n + k - 1)
            n += 8
        return (arr)

    # 性能测试
    def benchmark(self):
        self.di.cost("start------第一种方法")
        for key in self.key_map:
            self.key2array(self.get(key))
        self.di.cost("start------第二种方法")
        for key in self.key_map:
            self.key2array2(self.get(key))
        self.di.cost("start-----第三种方法")
        for key in self.key_map:
            self.key2array3(self.get(key))
        self.di.cost("end")

    def str2bin(self, str):
        return bin(int(str, 10))

    def encode(self, s):
        return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

    def decode(self, s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

# 测试
if __name__ == '__main__':
    bm = Bitmap()
    bm.init_db(1000)
    # print(bm.key2array(bm.get("user:vip")))
    # bm.key2array2(bm.get("test_a"))
    # bm.key2array3(bm.get("test_a"))
    # bm.benchmark()
