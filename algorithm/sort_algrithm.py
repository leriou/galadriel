class SortAlgorithm:

    def __init__(self):
        self.arr = [15, 9, 12, 10, 99, 8, 6, 76, 56, 4, 100, 34, 2, 98]
        self.len = len(self.arr)

    def insertsort(self):  # 插入排序
        lists = self.arr
        for i in range(1, self.len):
            key = lists[i]
            j = i - 1
            while j >= 0:
                if lists[j] > key:
                    lists[j + 1] = lists[j]
                    lists[j] = key
                j -= 1
        print(lists)

    def shellsort(self):  # 希尔排序
        count = self.len
        lists = self.arr
        step = 2
        group = count // step
        while group > 0:
            group = int(group)
            for i in range(0, group):
                j = i + group
                while j < count:
                    k = j - group
                    key = lists[j]
                    while k >= 0:
                        if lists[k] > key:
                            lists[k + group] = lists[k]
                            lists[k] = key
                        k -= group
                    j += group
            group /= step
        print(lists)

    def selectsort(self):  # 选择排序
        count = self.len
        lists = self.arr
        for i in range(0, count):
            min = i
            for j in range(i + 1, count):
                if lists[min] > lists[j]:
                    min = j
            lists[min], lists[i] = lists[i], lists[min]
        print(lists)

    def bubble_sort(self):  # 冒泡排序
        count = self.len
        lists = self.arr
        for i in range(0, count):
            for j in range(i + 1, count):
                if lists[i] > lists[j]:
                    lists[i], lists[j] = lists[j], lists[i]
        print(lists)

    def mergesort(self):
        r = self.merge(self.arr)
        print(r)

    def merge(self, lists):  # 归并排序
        if len(lists) <= 1:
            return lists
        num = len(lists) // 2
        left = self.merge(lists[:num])
        right = self.merge(lists[num:])
        i, j = 0, 0
        result = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result

    def quicksort(self):
        r = self.quick(self.arr, 0, self.len - 1)
        print(r)

    def quick(self, lists, left, right):  # 快速排序
        if left >= right:
            return lists
        key = lists[left]
        low = left
        high = right
        while left < right:
            while left < right and lists[right] >= key:
                right -= 1
            lists[left] = lists[right]
            while left < right and lists[left] <= key:
                left += 1
            lists[right] = lists[left]
        lists[right] = key
        self.quick(lists, low, left - 1)
        self.quick(lists, left + 1, high)
        return lists


class T(SortAlgorithm):
    pass


if __name__ == '__main__':
    m = T()
    m.mergesort()
