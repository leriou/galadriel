class Cal():

    def __init__(self):
        self.a = [3, 5, 8, 1, 5, 9]
        self.now = []

    def cal_earnings(self):
        tmp = 0
        for i in range(1, len(self.a)):
            if self.a[i] > self.a[i - 1]:
                earn = self.a[i] - self.a[i - 1]
                tmp = tmp + earn
                self.now.append(tmp)
            else:
                tmp = 0
        self.now.sort()
        l_e = len(self.now)
        if l_e >= 2:
            v = self.now[l_e - 1] + self.now[l_e - 2]
        elif l_e == 1:
            v = self.now[0]
        else:
            v = 0

        print(v)


class MoveZero:

    def move(self, arr):
        pos = 0
        for i in range(len(arr)):
            if arr[i]:
                arr[i], arr[pos] = arr[pos], arr[i]
                pos += 1
        print(arr)


if __name__ == '__main__':
    m = MoveZero()
    m.move([0, 1, 2, 0, 4, 6])
    c = Cal()
    c.cal_earnings()
