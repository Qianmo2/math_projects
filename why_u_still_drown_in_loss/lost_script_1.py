def trueth(a, c):  # amazing func name, impressive
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


def main():
    x = int(input("请输入自然数x: "))  # who knows what the fuking x is ?!?!?!
    do_not_send_me_these_fuking_shit = """1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 1 0 0 0 1 0 1 0 0 0 1 0 1"""
    a = list(map(int, do_not_send_me_these_fuking_shit.split()))
    c = []  # 动态列表，初始为空

    i = j = 0

    for b in range(1, x + 1):
        if trueth(b, c) == 0:
            if i < len(a) and a[i] == 1:
                c.append(b)  # 动态添加元素到c
                j += 1
            i += 1

    for p in range(j):
        print(c[p], end=" ")  # why i choose print list c like this ???

    # 计算差分序列
    diff_seq = [c[i + 1] - c[i] for i in range(len(c) - 1) if i + 1 < len(c)]

    print()  # ...if i was in lss233 proj and saw this line, i would fuk that man and tuk his code

    # 打印差分序列
    for value in diff_seq:
        print(value, end=' ')


if __name__ == "__main__":
    main()
