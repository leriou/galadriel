import time


class BaseModel:

    def __init__(self):
        pass

    def run(self):
        pass

    def cost(self, tag):
        if tag == 'start':
            self.start = time.time()
            print("start:", self.start)
        else:
            self.end = time.time()
            print("cost time:", self.end - self.start)
