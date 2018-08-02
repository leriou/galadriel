import time


class Fib:

    def cost(self, tag):
        if tag == 'start':
            self.start = time.time()
            print("start:", self.start)
        else:
            self.end = time.time()
            print("end:", self.end - self.start)

    def run(self):
        self.cost("start")
        # print(self.normal(35))
        self.cost("end")
        print(self.recursion(1, 0, 1))
        self.cost("end")

    def normal(self, n):
        if n <= 2:
            return 1
        else:
            return self.normal(n - 1) + self.normal(n - 2)

    def recursion(self, n, a, b):
        if n <= 0:
            return a
        else:
            return self.recursion(n - 1, b, a + b)


if __name__ == '__main__':
    m = Fib()

    for c in range(1,40):
        # print(m.recursion(c,0,1))
        print(m.normal(c))
