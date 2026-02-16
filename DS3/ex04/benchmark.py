from collections import Counter
import timeit

def to_dictionary_v1(numbers):
    dictionary={i: 0 for i in range(101)}
    for number in numbers:
        dictionary[number] += 1
    return dictionary

def top_ten_v1(numbers):
    a=to_dictionary_v1(numbers)
    return dict(sorted(a.items(),key=lambda item: item[1], reverse=True)[:10])

def to_dictionary_v2(numbers):
    #возращает значения только с ненулевым value
    return Counter(numbers)

def top_ten_v2(numbers):
    return dict(Counter(numbers).most_common(10))

def main():

    setup = '''
import random
from __main__ import to_dictionary_v1, top_ten_v1, to_dictionary_v2, top_ten_v2
n=[random.randint(0, 100) for _ in range(1000000)]
'''

    time = timeit.timeit(stmt='to_dictionary_v1(n)', setup=setup, number=100)
    print(f'my function: {time}')

    time = timeit.timeit(stmt='to_dictionary_v2(n)', setup=setup, number=100)
    print(f'Counter: {time}')

    time = timeit.timeit(stmt='top_ten_v1(n)', setup=setup, number=100)
    print(f'my top: {time}')

    time = timeit.timeit(stmt='top_ten_v2(n)', setup=setup, number=100)
    print(f"Counter's top: {time}")

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)



