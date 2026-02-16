import timeit
import sys
from functools import reduce

class Counter():
    def __init__(self):
        pass

    def approach_loop(self,n):
        sum=0
        for i in range(1, n+1):
            sum = sum + i * i
        return sum

    def approach_reduce(self,n):
        return reduce(lambda x, y: x + y*y, range(1, n+1),0)

    def choose(self,mode,n):
        if mode == "loop": return self.approach_loop(n)
        elif mode == "reduce": return self.approach_reduce(n)
        else: return None


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit()

    try:
        setup = '''
from __main__ import Counter
counter = Counter()
'''
        time = timeit.timeit(stmt=f'counter.choose("{sys.argv[1]}",{int(sys.argv[3])})', setup=setup, number = int(sys.argv[2]))
        print(time)

    except Exception as error:
        print(error)



