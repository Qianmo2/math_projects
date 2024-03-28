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

with open('paperfolding_sequence.txt', 'w') as file:
    file.write(str(a))
