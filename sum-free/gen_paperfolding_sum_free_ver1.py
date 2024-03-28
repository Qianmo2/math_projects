def can_add_to_c(a, c):
    """
    第一版改进意见：
    can_add_to_c函数通过双重循环检查a是否可以表示为c中任意两个元素的和
    这个过程非常耗时，特别是当c数组变得很大时
    可以通过使用一个集合来跟踪c中所有可能的和来优化这个过程，这样就可以在O(1)时间内检查a是否在这个集合中
    """
    i = 0
    n = 0
    while i < len(c) and c[i] != 0:
        j = 0
        while j < len(c) and c[j] != 0:
            if a == c[i] + c[j]:
                n += 1
            j += 1
        i += 1
    return n


def gen_paperfolding_seq():
    """
    第一版改进意见：
    这个函数生成一个纸折序列，但是它的实现相对直接且未经优化
    考虑到这个序列的特殊性质，我们可以尝试找到更高效的生成方式，但是在这个特定的问题中，这个函数的性能不是主要瓶颈（）
    """
    q = 100
    a = [0] * q
    a[0] = 1

    for i in range(1, q):
        if i % 4 == 0:
            a[i] = 1
        if i % 4 == 2:
            a[i] = 0

    for i in range(1, q):
        if (2 * i + 1) < q:
            a[2 * i + 1] = a[i]

    return a


def main():
    """
    第一版改进意见：
    可以通过更有效地管理c数组和相关的索引来减少不必要的计算
    """
    x = int(input("请输入自然数x："))
    a = gen_paperfolding_seq()
    c = []

    i = 0
    b = 1
    while len(c) < x:
        if can_add_to_c(b, c) == 0:
            if a[i % len(a)] == 1:
                c.append(b)
            i += 1
        b += 1

    print(f"sum-free序列为：\n{c}")
    diff_seq = [c[i + 1] - c[i] for i in range(len(c) - 1)]
    print(f"差分序列为：\n{diff_seq}")


if __name__ == "__main__":
    main()
