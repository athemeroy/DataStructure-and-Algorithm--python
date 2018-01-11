import random


def is_sorted(array):
    """
    用于断言某个列表已经被排序好
        assert(is_sorted(array)), 'this array is not sorted'

    :param array: 要被断言的列表
    :return: 是否排序好
    """
    for i in range(len(array) - 1):
        if array[i] > array[i + 1]:
            return False
    return True


def bubble_sort_a(array):
    """
    最初版本的冒泡排序，双层循环len(array) - 1次
    外层循环len(array) - 1次，原因是最后只剩下第一个元素，自动就位
    内层循环len(array) - 1次，原因是导数第二个元素和导数第一个元素比较之后就已经结束
    :param array: 要被排序的列表
    :return: 排序好的列表
    """
    for i in range(len(array) - 1):
        for j in range(len(array) - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def bubble_sort_b(array):
    """
    第二个版本的冒泡排序，外层循环len(array) - 1次，内层循环len(array)-1-i次
    这个版本的冒泡排序呈三角形状，每次循环长度递减，体现减而治之的思想
    外层循环len(array) - 1次，原因是最后只剩下第一个元素，自动就位
    内层循环len(array) - 1次，原因是事实上每次外层循环过后，最后一个元素就已经就位，下次不需要再处理这个元素
    :param array: 要被排序的列表
    :return: 排序好的列表
    """
    length = len(array)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def bubble_sort_c(array):
    """
    第三个版本的冒泡排序，外层循环len(array) - 1次，内层循环len(array)-1-i次
    但加入了一个flag，用于判断是否已经排序好了。
    有些列表可能在前半部分是有序的，但是根据上一个版本的冒泡排序，无论前面是否有序
    外层都至少要循环len(array) - 1 次，如果前面有序，白白比较了很多次
    这时如果用一个boolean变量来存放是否已经有序，每当外层循环一次，首先置为True
    一旦出现某次交换，则置为False，每次外层循环首先检查是否为True，如果为True，
    跳出循环直接返回，否则继续进行外层循环。达到减少外层循环次数的目的
    :param array: 要被排序的列表
    :return: 排序好的列表
    """
    length = len(array)
    flag = False
    for i in range(length - 1):
        if flag:
            return array
        else:
            flag = True
            for j in range(length - 1 - i):
                if array[j] > array[j + 1]:
                    flag = False
                    array[j], array[j + 1] = array[j + 1], array[j]
    return array


def bubble_sort_d(array):
    """
    第四个版本的冒泡排序 结合了前面的flag
    但是加入了一个“最后交换的索引”这个变量，这个变量用于记录最后一次交换的索引，
    在每次外层循环结束之后，事实上最后一次交换的索引后面的所有元素已经就序
    只需要关注前面的元素即可，体现了更加明确的减而治之的思想
    :param array: 待排序的列表
    :return:排序后的列表
    """
    hi = len(array)
    flag = False
    while not flag:
        flag = True
        j = 0
        while j < hi - 1:
            if array[j] > array[j + 1]:
                flag = False
                array[j], array[j + 1] = array[j + 1], array[j]
                last_swap = j + 1
            j += 1
        hi = last_swap
    return array


def main():
    l = random.sample(range(1000), 300)
    print(l)
    bubble_sort_d(l)
    print(l)
    assert (is_sorted(l)), 'this array is not sorted'


if __name__ == '__main__':
    main()
