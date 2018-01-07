class Vector:
    def __init__(self, capacity=3, default_capacity=3):
        # 向量的容纳空间
        self._default_capacity = default_capacity
        self._capacity = capacity
        # 向量的大小
        self._size = 0
        # 向量的内容
        self._elem = [None] * self._capacity
        # 向量的装填因子
        self._load_factor = self._size / self._capacity

    def _expand(self):
        # 如果存储空间不够了，扩容
        if self._size < self._capacity:
            return
        # 这里应该找一块内存存进去
        old_size = self._size
        old_elem = self._elem
        self.__init__(max(self._default_capacity, self._capacity << 1))
        for i in range(old_size):
            self._elem[i] = old_elem[i]
            self._size += 1
        del old_elem
        return

    def _shrink(self):
        # 如果存储空间过于富裕了，缩容
        if self._size > self._capacity >> 1 or self._capacity == self._default_capacity:
            return
        # 这里应该找一块内存存进去
        old_size = self._size
        old_elem = self._elem
        # self.__init__(max(self._default_capacity, self._capacity >> 1))
        self.__init__(self._capacity >> 1)
        for i in range(old_size):
            self._elem[i] = old_elem[i]
            self._size += 1
        del old_elem
        if self._size < self._capacity >> 1:
            self._shrink()
        return

    def __getitem__(self, item):
        return self.get(item)

    def get(self, index):
        return self._elem[index]

    def put(self, index, value):
        self._elem[index] = value

    def append(self, elem):
        self._expand()
        self._elem[self._size] = elem
        self._size += 1

    def insert(self, index, elem):
        # 如有必要，扩容
        self._expand()
        # 所有元素后移一位（从后向前，否则会覆盖元素）
        for i in range(index, self._size + 1)[::-1]:
            self._elem[i + 1] = self._elem[i]
        self._elem[index] = elem
        self._size += 1
        return

    @property
    def size(self):
        return self._size

    def remove(self, lo, hi=None):
        # 为什么不通过反复移除一个元素实现删除很多元素呢？
        # 如果反复调用的话，会导致每次都要把后继移动一格，复杂度到了o(n^2)
        # 而现在这种情况，只需要移动一次 o(n)
        if hi:
            if hi > self.size:
                raise IndexError('向量超过上界')
            cur_lo = lo
            cur_hi = hi
            while cur_lo < self._size:
                if cur_hi < self._size:
                    self._elem[cur_lo] = self._elem[cur_hi]
                    cur_hi += 1
                else:
                    self._elem[cur_lo] = None
                cur_lo += 1
            self._size -= hi - lo
            # 如有必要，缩容
            self._shrink()
            return hi - lo
        else:
            lo_elem = self._elem[lo]
            self.remove(lo, lo + 1)
            return lo_elem

    def search(self, value, search_range=None):
        if search_range is None:
            search_range = (0, self._size)
        else:
            assert (type(search_range) == list or type(search_range) == tuple) \
                   and len(search_range) == 2, '需要2元组'
        # print(f'searching for {value}')
        hi = search_range[1] - 1
        while hi >= search_range[0]:
            if self._elem[hi] == value:
                return hi
            hi -= 1
        return -1

    def deduplicate(self):
        # print('deduplicating')
        cur = 0
        while cur < self.size:
            if self.search(self._elem[cur], [0, cur]) >= 0:
                # print(f'found duplicate {self._elem[cur]}')
                self.remove(cur)
            else:
                cur += 1

        return self

    def traverse(self, callback):
        cur = 0
        while cur < self.size:
            self._elem[cur] = callback(self._elem[cur])
            cur += 1

    def disordered(self):
        cur = 1
        while cur < self.size:
            if self._elem[cur] < self._elem[cur - 1]:
                return True
        return False


    def __repr__(self):
        return f"<Vector elem:{self._elem}>"


if __name__ == '__main__':
    vec = Vector()
    import random

    for i in range(1000):
        vec.append(random.randint(0, 200))
    print('removing 3')
    vec.remove(3)
    print('removing 2,80')
    print(vec.remove(2, 80))
    print(vec)
    print('searching for 1 in [10,20)')
    print(vec.search(1, [10, 20]))
    print(f'searching for {vec[15]} in [10,20)')
    print(vec.search(vec[15], [10, 20]))
    print(vec)
    print(f'vec.size : {vec.size}')
    print('deduplicating')
    print(vec.deduplicate())
    print(f'vec.size: {vec.size}')
    print('traverse plus one')
    vec.traverse(lambda x: x+1)
    print(vec)
