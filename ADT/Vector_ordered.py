class Vector_ordered():
    def __init__(self, capacity=2, default_capacity=2):
        self._capacity = capacity
        self._default_capacity = default_capacity
        self._size = 0
        self._elem = [None] * self._capacity

    @property
    def size(self):
        return self._size

    def _expand(self):
        if self.size < self._capacity:
            return
        old_size = self.size
        old_elem = self._elem
        self.__init__(self.size << 1)
        i = 0
        while i < old_size:
            self._elem[i] = old_elem[i]
            i += 1
        self._size = old_size
        return

    def disordered(self):
        i = 0
        while i < self.size - 1:
            if self._elem[i] > self._elem[i + 1]:
                return True
            i += 1
        return False

    def shrink(self, position):
        """
        从postion开始的所有元素直接截断
        :param position: 被截断的第一个元素
        :return: 截断后的新向量
        """
        old_elem = self._elem
        i = 0
        self.__init__(position)
        while i < position:
            self._elem[i] = old_elem[i]
            i += 1
        self._size = position
        return

    def remove(self, lo, hi=None):
        # 为什么不通过反复移除一个元素实现删除很多元素呢？
        # 如果反复调用的话，会导致每次都要把后继移动一格，复杂度到了o(n^2)
        # 而现在这种情况，只需要移动一次 o(n)
        if hi:
            if hi > self.size:
                raise IndexError('向量超过上界')
            cur_lo = lo
            cur_hi = hi
            while cur_hi < self._size:
                self._elem[cur_lo] = self._elem[cur_hi]
                cur_hi += 1
                cur_lo += 1
            self.shrink(cur_lo)
            return hi - lo
        else:
            lo_elem = self._elem[lo]
            self.remove(lo, lo + 1)
            return lo_elem

    def deduplicate(self):
        """
        删除列表中的重复元素
        因为是有序向量，所以用两个指针对应：在两个指针数值相等时，右指针向右移动
        当遇到不同的元素时，左指针右移一格，将左指针对应的元素值赋值为右指针的值
        当右指针达到向量末尾，截断左指针后方的所有元素
        :return:删除后的原列表
        """
        assert (not self.disordered())
        i = 0
        j = 1
        while j < self.size:
            if self._elem[i] == self._elem[j]:
                j += 1
            else:
                i += 1
                self._elem[i] = self._elem[j]
        return self.shrink(i + 1)

    def search(self, value):
        """
        使用二分查找（终板）查找某个值在向量中的秩
        :param value: 要查找的值
        :return: 不大于value的最后一个元素的位置
        """
        return self.search_range(value, 0, self.size)

    def search_range(self, value, lo, hi):
        # print(f'now lo {lo} hi {hi} mid {(hi+lo) >> 1}')
        while hi > lo:
            mid = (hi + lo) >> 1
            if value < self._elem[mid]:
                hi = mid
            else:
                lo = mid + 1
        # print(lo - 1)
        return lo - 1

    def linear_search(self, value):
        """
        查找某个值在向量中的秩
        :param value: 要查找的值
        :return: 不大于value的最后一个元素的位置
        """
        i = 0
        while i < self.size:
            if self._elem[i] <= value:
                i += 1
            else:
                return i - 1
        return i - 1

    def binary_search(self, value):
        """
        二分查找
        递归调用下面的binary_search_range函数，达到查找的目的。

        这个查找方式虽然已经是1.5logn级别，但是还是有问题：
        转向左右分支的比较次数不同，但是递归深度相同。 向左查找只需要一次比较，️而向右查找需要两次。
        所以可以用fibonacci查找来优化
        :param value:要查找的值
        :return:索引 或者找不到的-1
        """
        return self.binary_search_range(value, 0, self.size)

    def binary_search_range(self, value, lo, hi):
        if hi == lo:
            return -1
        i = ((hi - lo) >> 1) + lo
        # print(i)
        if value < self._elem[i]:
            # print(f'not found, next:{lo}, {i}')
            return self.binary_search_range(value, lo, i)
        elif value > self._elem[i]:
            # print(f'not found, next:{i+1}, {hi}')
            return self.binary_search_range(value, i + 1, hi)
        else:
            # print(f'found {i}')
            return i

    def fib_search(self, value):
        return self.fib_search_range(value, 0, self.size)

    def fib_search_range(self, value, lo, hi):
        if hi == lo:
            return -1
        i = int((hi - lo) * 0.618) + lo
        # print(i)
        if value < self._elem[i]:
            # print(f'not found, next:{lo}, {i}')
            return self.binary_search_range(value, lo, i)
        elif value > self._elem[i]:
            # print(f'not found, next:{i+1}, {hi}')
            return self.binary_search_range(value, i + 1, hi)
        else:
            # print(f'found {i}')
            return i

    def binary_search_improve(self, value):
        return self.binary_search_improve_range(value, 0, self.size)

    def binary_search_improve_range(self, value, lo, hi):
        # 下面的是递归算法 可以改为迭代
        # if hi == lo:
        #     return -1
        # i = ((hi - lo) >> 1) + lo
        # # print(i)
        # if value < self._elem[i]:
        #     # print(f'not found, next:{lo}, {i}')
        #     return self.binary_search_range(value, lo, i)
        # else:
        #     # print(f'not found, next:{i+1}, {hi}')
        #     return self.binary_search_range(value, i, hi)
        # print(f"finding {value}")
        while hi - lo != 1:
            mid = (hi + lo) >> 1
            if value < self._elem[mid]:
                hi = mid
                # print(f'now left:{lo}, {hi}')

            else:
                lo = mid
                # print(f'now right:{lo}, {hi}')

        if self._elem[lo] == value:
            return lo
        else:
            return -1

    def insert(self, value):
        self._expand()
        # print(f'expanded {self}')
        position = self.search(value)
        cur = self.size
        # print(f'position:{position},cur:{cur}')
        while cur > position:
            self._elem[cur] = self._elem[cur - 1]
            cur -= 1
        # print(f'inserted { value } to {cur + 1}')
        self._elem[cur + 1] = value
        self._size += 1
        return

    def __repr__(self):
        return f"<Vector elem:{self._elem}>"


def main():
    vec = Vector_ordered()
    import random

    vec.insert(3)
    # print(vec)
    for i in range(10000):
        vec.insert(random.randint(0, 5500))

    vec.insert(5)
    vec.insert(5)
    vec.insert(5)
    # vec.insert(5)
    # vec.insert(5)
    # print(vec.size, vec)
    # print(vec.search(5))
    vec.remove(2, 9990)
    vec.deduplicate()
    print(vec)

    # print(vec.size, vec)
    # print(vec.search(5))
    # vec.insert(65)
    # print(vec)
    # vec.insert(5)
    # vec.insert(5)
    # print(vec)
    # vec.insert(4)
    # print(vec)


if __name__ == '__main__':
    main()
