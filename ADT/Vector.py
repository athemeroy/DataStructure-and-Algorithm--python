class Vector:
    def __init__(self, capacity=2, default_capacity=2):
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

    def _shrink(self, position):
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

    def __getitem__(self, item):
        return self.get(item)

    def get(self, index):
        return self._elem[index]

    def put(self, index, value):
        assert (index < self.size), '向量越界'
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
            while cur_hi < self._size:
                self._elem[cur_lo] = self._elem[cur_hi]
                cur_hi += 1
                cur_lo += 1
            self._shrink(cur_lo)
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
        cur = 0
        while cur < self.size - 1:
            if self._elem[cur] > self._elem[cur + 1]:
                return True
            cur += 1
        return False

    def bubble_sort_a(self):
        """
        第一个版本的起泡排序
        每一趟循环，在尾部终止，因为每次冒泡最大的都已经就绪
        :return: 排序好的向量
        """

        def swap(array, a, b):
            array._elem[a], array._elem[b] = array._elem[b], array._elem[a]

        i = 0
        while i < self.size - 1:
            j = 0
            while j < self.size - 1 - i:
                if self._elem[j] > self._elem[j + 1]:
                    # print(f'{self._elem[j]} > {self._elem[j + 1]} swaping')
                    swap(self, j, j + 1)
                    # else:
                    # print(f'{self._elem[j]} <= {self._elem[j + 1]} maintain')

                # print(self)
                j += 1
            i += 1
            # print(f'now i = {i}')
        assert (not self.disordered())
        return

    def bubble_sort_b(self):
        """
        第二个版本的起泡排序
        因为有些时候可能前面的部分早就被排好序了，但是因为冒泡排序不检查前面是否排好序
        机械地进行接下来的操作，所以可以定义一个flag：sorted
        只有在flag被放倒的时候才会进行下一趟
        每一趟都把
        :return: 排序好的向量
        """

        def swap(array, a, b):
            array._elem[a], array._elem[b] = array._elem[b], array._elem[a]

        i = 0
        is_sorted = False
        while (not is_sorted) and i < self.size - 1:
            is_sorted = True
            j = 0
            while j < self.size - 1 - i:
                if self._elem[j] > self._elem[j + 1]:
                    # print(f'{self._elem[j]} > {self._elem[j + 1]} swaping')
                    swap(self, j, j + 1)
                    is_sorted = False
                    # else:
                    # print(f'{self._elem[j]} <= {self._elem[j + 1]} maintain')

                # print(self)
                j += 1
            i += 1
            # print(f'now i = {i}')
        assert (not self.disordered())
        return

    def bubble_sort_c(self):
        """
        第三个版本的起泡排序
        第二个版本考虑了如果前面本身是有序的 或者提前已经排好序了
        但是如果后面是有序的，依然会反复地对后面进行交换（这本身是没有必要的）

        只要记录最后一次扫描交换的位置，就可以在下一次扫描交换的时候少做很多操作
        :return: 排序好的向量
        """

        def swap(array, a, b):
            array._elem[a], array._elem[b] = array._elem[b], array._elem[a]

        i = 0
        is_sorted = False
        last_swap = self.size - 1
        hi = self.size - 1
        # print(self)
        # print('*'*50)
        # while (not sorted) and i < self.size:
        while not is_sorted:
            is_sorted = True
            j = 0
            while j < hi:
                if self._elem[j] > self._elem[j + 1]:
                    # print(f'{self._elem[j]} > {self._elem[j + 1]} swapping')
                    swap(self, j, j + 1)
                    last_swap = j + 1
                    is_sorted = False
                # else:
                    # print(f'{self._elem[j]} <= {self._elem[j + 1]} maintaining')
                j += 1
                # print(self)
            # i += 1
            hi = last_swap
            # print(f'now i = {i}, hi = {hi}')
        assert (not self.disordered())
        return self

    def merge_sort(self):
        """
        归并排序
        :return: 排序好的向量
        """

        def merge(left, right):
            """
            归并排序的合并部分
            :param left: 左侧向量
            :param right: 右侧向量
            :return: 按照大小合并之后的向量
            """
            if right is None:
                return left
            merged_result = Vector()
            i = 0
            j = 0
            for k in range(left.size + right.size):
                if i == left.size:
                    merged_result.append(right[j])
                    j += 1
                elif j == right.size:
                    merged_result.append(left[i])
                    i += 1
                elif left[i] < right[j]:
                    merged_result.append(left[i])
                    i += 1
                else:
                    merged_result.append(right[j])
                    j += 1
            return merged_result

        # 用来分割向量， 生成一个包含仅由一个一个元素组成的向量的向量
        divided_vector = Vector()
        i = 0
        while i < self.size:
            atom_vector = Vector()
            atom_vector.append(self[i])
            divided_vector.append(atom_vector)
            i += 1
        # 开始合并， 只要合并之后的向量的长度依然超过1
        while divided_vector.size > 1:
            i = 0
            merged_vector = Vector()
            # 就用一个新的向量组成两两合并之后的向量
            while i < divided_vector.size:
                merged_vector.append(merge(divided_vector._elem[i],
                                           divided_vector._elem[i + 1]))
                i += 2
            # print(f"done {merged_vector.size},{merged_vector}")
            # 用一个新的向量组成两两合并之后的向量
            divided_vector = merged_vector
        # 因为上面是最后append了merge之后的结果，所以最后得到的向量一定是Vector[Vector, None]的形式
        # 所以最后取向量的第一个就可以了
        return divided_vector[0]

    def __repr__(self):
        return f"<Vector elem:{self._elem}>"


if __name__ == '__main__':
    vec = Vector()
    import random

    for i in range(30):
        vec.append(random.randint(0, 400))

    # for i in range(30)[::-1]:
    #     vec.append(i)
    # print('removing 3')
    # vec.remove(3)
    # print(vec)
    # print('removing 2,8')
    # print(vec.remove(2, 8))
    # print(vec)
    print(vec.bubble_sort_c())

    def a():
        v = Vector()
        for i in range(1000):
            v.append(random.randint(0,300))
        v.bubble_sort_a()

    def b():
        v = Vector()
        for i in range(1000):
            v.append(random.randint(0,300))
        v.bubble_sort_b()

    def c():
        v = Vector()
        for i in range(1000):
            v.append(random.randint(0,300))
        v.bubble_sort_c()

    def d():
        v = Vector()
        for i in range(1000):
            v.append(random.randint(0,300))
        v.merge_sort()


    # print('searching for 1 in [10,20)')
    # print(vec.search(1, [10, 20]))
    # print(f'searching for {vec[15]} in [10,20)')
    # print(vec.search(vec[15], [10, 20]))
    # print(vec)
    # print(f'vec.size : {vec.size}')
    # print('deduplicating')
    # print(vec.deduplicate())
    # print(f'vec.size: {vec.size}')
    # print('traverse plus one')
    # vec.traverse(lambda x: x+1)
    # print(vec)
    # vec.append(1)
    # vec.append(0)
    # print(vec.divide(vec))
    # print(vec.merge(vec.divide(vec)))
    # print(vec.size)
    # a = vec.merge_sort()
    # print(vec.disordered())
    # print(a)
    # print(a.size)
    # print(a.disordered())
    # print(a.disordered())
