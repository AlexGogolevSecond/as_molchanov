from time import time


# g = gen('alex')

def gen_timename():
    while True:
        pattern: str = 'file-{}.jpeg'
        t = int(time() * 1000)

        yield pattern.format(str(t))

        summa: int = 222 * 333
        print(summa)

# g = gen_timename()
def gen1(s):
    for i in s:
        yield i

def gen2(n):
    for i in range(n):
        yield i

g1 = gen1('alex')
g2 = gen2(4)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
