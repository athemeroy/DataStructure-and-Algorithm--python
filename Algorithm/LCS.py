from memo import memo

@memo
def LCS1(l1, l2):
    """
    寻找l1(0,n) l2(0,m)的最长子序列。
    算法1：
        递归求解：
        (1)如果l1 l2其中一个长度为0，返回''（递归机）
        (2)如果l1[n] == l2[m] == 'x'(减而治之)
        return LCS1(l1[0:n-1],l2[0,m-1]) + 'x'
        (3)如果l1[n] != l2[m](分而治之)
        求解LCS1(l1[0:n-1],l2[0,m])和LCS1(l1[0:n], l2[0,m-1])
        选择更长的一个
        
        如果不用memo装饰器
        这几乎不是一个算法 因为如果出现了第三种情况，
        会把规模扩大为几乎原来的两倍，
        这个时候如果是方形，复杂度是2^n
        without memo
        10 loops, best of 3: 33.4 ms per loop
        with memo
        1000000 loops, best of 3: 312 ns per loop
    """

    if len(l1) == 0 or len(l2) == 0:
#        print('递归机')
        return ''
    elif l1[-1] == l2[-1]:
#        print('找到一致', l1[-1])
        return LCS1(l1[:-1], l2[:-1]) + l1[-1]
    else:
#        print('找到不一致')
        left = LCS1(l1[:-1], l2)
        right = LCS1(l1, l2[:-1])
        if len(left) >= len(right):
            # 这里会出问题:
            # 如果最后左和右一样长, 最后只会输出一个结果
            return left
        else:
            return right
        
@memo
def LCS2(l1, l2):
    """
    寻找l1(0,n) l2(0,m)的最长子序列。
    算法2:
        动态规划的想法,自下而上进行求解
        对于每一个从前向后的子序列,考虑到底是减而治之还是分而治之
        如果没有memo:
            化递归为迭代
            对比算法1没有memo的情况,少做了很多无用功
            1000000 loops, best of 3: 1.65 µs per loop
        如果有memo:
            因为如果是分而治之的情况,前面的两种情况一定已经被计算过
            所以依然可以通过memo来加速
            1000000 loops, best of 3: 315 ns per loop
        
    """
    if len(l1) == 0 or len(l2) == 0:
#        print('递归机')
        return ''
    elif l1[0] == l2[0]:
#        print('找到一致', l1[-1])
        return l1[0] + LCS1(l1[1:], l2[1:])
    else:
#        print('找到不一致')
        left = LCS1(l1[1:], l2)
        right = LCS1(l1, l2[1:])
        if len(left) >= len(right):
#             这里会出问题:
#             如果最后左和右一样长, 最后只会输出一个结果
            return left
        else:
            return right

if __name__ == "__main__":
    print(LCS2('educational', 'advantage'))
