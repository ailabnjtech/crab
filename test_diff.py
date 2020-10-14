import math


def euclid_dist(x, y):
    return math.sqrt(sum([(a - b)**2 for (a, b) in zip(x, y)]))


f = open('testxml-ds.csv', 'rb')
rs = f.readlines()
names = [str(r.strip().split(b',')[0]) for r in rs]
rows = [[float(i) for i in r.strip().split(b',')[1:]] for r in rs]
f.close()


rc = len(rows)
with open('test_diff.csv', 'wb') as f:
    for i in range(rc):
        for j in range(rc):
            if i == j:
                continue
            f.write('{}, {}, {}, {}\n'.format(names[i], names[j], euclid_dist(rows[i][:15], rows[j][:15]), euclid_dist(rows[i][15:], rows[j][15:])).encode())


