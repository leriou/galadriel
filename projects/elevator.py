#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
电梯调度算法

功能:
1. 将乘客送往目的地楼层,支持多乘客
2. 支持多部电梯,支持自定义电梯楼层

电梯运行方向 True:向上 False:向下

电梯送人的详细过程:

1. 按按钮,通知中控,有人要叫电梯
2. 中控根据乘客需求和当前电梯的运行,选择电梯,并调整电梯的运行线路
3. 电梯按照线路运行,到那一层停,每次停都进行上乘客和下乘客的活动

"""
import time


class Passenger:  # 乘客

    def __init__(self, p):
        self._id = p["id"]      # 乘客的id
        self.name = p['name']    # 乘客名称
        self.s = p['s']          # 乘客开始楼层
        self.e = p['e']          # 目的地楼层
        self.direction = (self.s < self.e)  # 要去的方向 True 上 False 下
        self.weight = p['weight']  # 乘客体重


class Elevator:  # 电梯

    def __init__(self, e):
        self._id = e["id"]    # 电梯的id
        self.name = e['name']  # 电梯名称
        self.state = True      # 电梯的状态  False 损坏
        self.load = e['load']  # 电梯的最大负载
        self.load_used = 0     # 电梯当前负载
        self.available_floor = e['available_floor']  # 电梯可达楼层
        self.current_floor = 1   # 电梯的当前楼层
        self.destination_floor = 1  # 电梯的目的地楼层
        self.running = False            # 电梯的运行状态 是运行中还是 暂停
        self.direction = True  # 运行方向  True 向上   False 向下
        self.passengers = []  # 当前运送的乘客
        self.invited_passengers = []  # 要去接的乘客
        self.sending_line = []  # 电梯的运送线路


class Controller:  # 中心调度器

    def __init__(self):
        self.waiting = []  # 等待的乘客
        self.sending = []  # 运送的乘客
        self.arrving = []  # 到达的乘客
        self.elevators = []  # 电梯
        self.running_elevators = []  # 运行中的电梯
        self.stoping_elevators = []  # 待命中的电梯
        self.delete = []     # 待删除的被分配过的乘客

    def set_passenger(self, l):  # 添加所有乘客
        for i in l:
            self.waiting.append(i)

    def set_elevator(self, l):  # 添加所有电梯
        for e in l:
            self.elevators.append(e)
            self.stoping_elevators.append(e)

    def start_elevator(self, e):  # 启动一部电梯
        e.running = True       # 将电梯标记为运行中,非待命
        # 将电梯标记为运行中
        if e in self.stoping_elevators:
            self.stoping_elevators.remove(e)
        if e not in self.running_elevators:
            self.running_elevators.append(e)  # 将电梯添加到运行中的列表
        print("电梯 %s 启动" % e.name)

    def stop_elevator(self, e):  # 停掉一部电梯
        e.running = False
        if e not in self.stoping_elevators:
            self.stoping_elevators.append(e)
        if e in self.running_elevators:
            self.running_elevators.remove(e)
        print("电梯 %s 停止" % e.name)

    def genarate_line(self, e, c):  # 根据电梯和用户生成线路和方向
        for f in range(min(e.current_floor, c.s), max(c.s, e.current_floor) + 1):
            e.sending_line.append(f)
        e.sending_line = list(set(e.sending_line))  # 去重
        # 确定方向
        if len(e.invited_passengers):
            e.direction = (e.current_floor <= c.s)
        # 根据方向确定目的楼层
        if e.direction == True:
            e.destination_floor = max(e.sending_line)
        else:
            e.destination_floor = min(e.sending_line)

        # print("线路")
        # print(e.sending_line)
        # print("方向 %s" % e.direction)

    def assign_passenger_to_elevator(self, c, e):  # 把一个乘客分配给一个电梯
        '''
         更新中心控制器的状态
        '''
        self.delete.append(c)   # 删除乘客, 不能使用waiting直接删除,会导致列表循环出问题
        self.sending.append(c)  # 将乘客加入正在运送的列表
        self.start_elevator(e)  # 启动这部电梯
        '''
        更新电梯的状态
        '''
        e.invited_passengers.append(c)  # 将乘客加入电梯的等待运送的列表
        self.genarate_line(e, c)
        print("由 %s 运送 乘客 %s" % (e.name, c.name))

    def choose_elevator(self, c):  # 为乘客选择电梯并分配
        for e in self.running_elevators:
            # 检查所有可到达乘客开始楼层和结束楼层的电梯
            if c.s in e.available_floor and c.e in e.available_floor:
                # return self.assign_passenger_to_elevator(c, e)
                # 检查是否有跟乘客需求方向相同并且能顺路载客的电梯
                if e.direction == c.direction:
                    if e.direction == True:
                        # 如果乘客和电梯都要向上,并且电梯未到达乘客所在楼层
                        if c.s > e.current_floor:
                            return self.assign_passenger_to_elevator(c, e)
                    else:
                        # 如果乘客和电梯都要向下,并且电梯未到达乘客所在的楼层
                        if c.s < e.current_floor:
                            return self.assign_passenger_to_elevator(c, e)
        # 运行中的电梯找不到合适的,从待命中的电梯找
        for e in self.stoping_elevators:
            if c.s in e.available_floor and c.e in e.available_floor:
                return self.assign_passenger_to_elevator(c, e)
            else:
                print("找不到合适的电梯运送乘客" + c.name + " 从 " + str(c.s) + "到" + str(c.e))
                return

    def move(self, e):  # 电梯e 移动
        # for c in self.waiting:
        #     print("等待中的:%s" % c.name)
        # 将到站的乘客送下去
        for c in e.passengers:
            if c.e == e.current_floor:
                # 乘客到了
                e.passengers.remove(c)
                self.arrving.append(c)
                self.sending.remove(c)
                log = e.name + " 把乘客 " + c.name + " 送到" + str(c.e) + "层"
                print(log)
                if len(e.passengers) == 0:  # 没有乘客就不送
                    self.stop_elevator(e)
                    return True

        # 检查是否有等待中的在本楼层的乘客
        for c in e.invited_passengers:
            if c.s == e.current_floor:
                e.invited_passengers.remove(c)
                e.passengers.append(c)
                print("在 " + str(e.current_floor) + "层 接到乘客" + c.name)

        # 根据当前线路开始运动
        # print(e.sending_line)

        # print("当前楼层: %d" % e.current_floor)
        # print("当前目标楼层 %d" % e.destination_floor)
        # print("当前方向 %s" % e.direction)
        if len(e.sending_line) > 0 and e.current_floor in e.sending_line:
            e.sending_line.remove(e.current_floor)
        if len(e.sending_line) == 0:
            # 重新设计线路 从当前楼层和乘客所有的目的地楼层中 选取最大值和最小值
            tmp_list = []
            for c in e.passengers:
                tmp_list.append(c.e)
            # 确定新方向
            if len(tmp_list) <= 0:
                return False
            e.direction = (max(tmp_list) > e.current_floor)
            if e.direction == True:
                e.destination_floor = max(tmp_list)
            else:
                e.destination_floor = min(tmp_list)
            tmp_list.append(e.current_floor)
            for n in range(min(tmp_list), max(tmp_list)):
                e.sending_line.append(n)

        if e.direction == True:
            # 向上的电梯将当前楼层+1
            e.current_floor = e.current_floor + 1
        else:
            # 向下的将当前楼层-1
            e.current_floor = e.current_floor - 1
        # 检查是否到了最顶或最底
        if (e.current_floor == e.destination_floor) and len(e.passengers) > 0:
            e.direction = not(e.direction)

    def alloc(self):  # 为乘客分配电梯
        for c in self.waiting:
            # print(" 乘客 %s 方向 %s" % (c.name, c.direction))
            self.choose_elevator(c)
        for c in self.delete:
            if c in self.waiting:
                self.waiting.remove(c)
        # self.report()

    def send(self):  # 送乘客
        for e in self.elevators:
            run = True  # 此次电梯是否运行
            if e.state:  # 未损坏的电梯
                if e.running == True and (e.current_floor != e.destination_floor):
                    run = True
                else:
                    if len(e.passengers) > 0:
                        run = True
            if run:
                self.move(e)

    def run(self):  # 主循环
        self.cost("start")
        while self.check_elevator_state():
            self.alloc()  # 中控检查是否有waiting中的乘客
            # return
            self.send()  # 处理sending中的乘客
            time.sleep(0.1)
        self.cost("end")

    def check_elevator_state(self):  # 检查电梯是否还需要运行,如果还有等待的乘客或者正在运送的乘客继续
        return len(self.waiting) != 0 or len(self.sending) != 0

    def report(self):
        log = "当前有" + str(len(self.elevators)) + "部电梯可用"
        for c in self.sending:
            print("现在正在运送乘客 " + c.name)
        for e in self.running_elevators:
            print("电梯" + e.name + "正在运行: 方向-" + str(e.direction) + " 目前正在-" +
                  str(e.current_floor) + ";目标楼层-" + str(e.destination_floor))
        for e in self.stoping_elevators:
            print("电梯" + e.name + "正在" + str(e.current_floor) + "待命")

    def cost(self, flag):  # 耗时
        if flag == "start":
            self.start_time = time.time()
        elif flag == "end":
            print("cost time: %s s" % (time.time() - self.start_time))

    def test(self):
        e = self.elevators[0]
        c1 = self.waiting[0]
        c2 = self.waiting[1]
        # c3 = self.waiting[1]

        self.genarate_line(e, c1)
        self.genarate_line(e, c2)
        # self.genarate_line(e, c3)
        print(e.sending_line)
        # self.genarate_line()


if __name__ == '__main__':
    customer1 = {"id": 1, "name": "c1", "s": 1, "e": 16, 'weight': 100}  # passeger 1
    customer2 = {"id": 2, "name": "c2", "s": 10, "e": 5, 'weight': 100}  # passenger 2
    customer3 = {"id": 3, "name": "c3", "s": 15, "e": 3, 'weight': 100}  # passenger 3
    customer4 = {"id": 4, "name": "c4", "s": 11, "e": 15, 'weight': 100}  # passenger 3
    customer5 = {"id": 5, "name": "c5", "s": 14, "e": 7, 'weight': 100}  # passenger 3
    customer6 = {"id": 6, "name": "c6", "s": 1, "e": 9, 'weight': 100}  # passenger 3
    elevator1 = {
        "id": 1,
        "name": "e1",
        "load": 1000,
        "available_floor": [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }
    elevator2 = {
        "id": 2,
        "name": "e2",
        "load": 1000,
        "available_floor": [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }
    elevator3 = {
        "id": 3,
        "name": "e3",
        "load": 1000,
        "available_floor": [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    }

    c = Controller()
    e1 = Elevator(elevator1)
    e2 = Elevator(elevator2)
    e3 = Elevator(elevator3)
    clist = []

    clist.append(Passenger(customer1))
    clist.append(Passenger(customer2))

    clist.append(Passenger(customer3))
    clist.append(Passenger(customer4))

    clist.append(Passenger(customer5))
    clist.append(Passenger(customer6))

    c.set_elevator([e1])
    c.set_passenger(clist)
    # c.test()
    c.run()
