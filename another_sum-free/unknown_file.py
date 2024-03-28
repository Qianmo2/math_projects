a = [0, 1]
b = [0, 1]
i = 1
j = 1

max_value = int(input("请输入一个整数："))

while j <= i <= max_value:
    if a[j] % 2 == 1:
        i += 1
        # 确保列表足够长
        if i >= len(b):
            b.append(a[j] + 1)
        else:
            b[i] = a[j] + 1
    if a[j] % 2 == 0:
        i += 1
        # 确保列表足够长
        if i >= len(b):
            b.append(a[j])
        else:
            b[i] = a[j]
        i += 1
        # 确保列表足够长
        if i >= len(b):
            b.append(a[j] + 1)
        else:
            b[i] = a[j] + 1
    # 扩展 a 列表以匹配 b 的长度
    if i >= len(a):
        a.extend([0] * (i - len(a) + 1))
    for k in range(j, i + 1):
        a[k] = b[k]
    j += 1

print(b)

with open(f'output_list_n={max_value}.txt', 'w') as file:
    file.write(str(b))
