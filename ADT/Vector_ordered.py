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

    def search(self, value):
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

    def insert(self, value):
        self._expand()
        # print(f'expanded {self}')
        position = self.search(value)
        cur = self.size
        # print(f'position:{position},cur:{cur}')
        while cur > position:
            self._elem[cur] = self._elem[cur - 1]
            cur -= 1
        print(f'inserted { value } to {cur + 1}')
        self._elem[cur + 1] = value
        self._size += 1
        return

    def __repr__(self):
        return f"<Vector elem:{self._elem}>"


if __name__ == '__main__':
    vec = Vector_ordered()
    import random
    for i in range(100000):
        vec.insert(random.randint(0, 50))
    print(vec.size)
    # vec.insert(65)
    # print(vec)
    # vec.insert(5)
    # vec.insert(5)
    # print(vec)
    # vec.insert(4)
    # print(vec)
