import timeit

#set
#startswith, endswith

class Search():
    def __init__(self, emails):
        self.emails = emails

    def loop(self):
        gmail=[]
        for i in self.emails:
            if i.endswith('@gmail.com'):
                gmail.append(i)
        return gmail

    def list_comprehension(self):
        return [i for i in self.emails if i.endswith('@gmail.com')]

    def search_map(self):
        #return map(lambda i: i if i.endswith('@gmail.com') else None, self.emails) быстрее,
        #тк только возращает объект map, а действия с ним производит только при взаимодействии(итерации) с ним
        return list(map(lambda i: i if i.endswith('@gmail.com') else None, self.emails))


if __name__ == '__main__':
    try:

        setup = '''
from __main__ import Search
emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
search = Search(emails)
'''

        loop_time = timeit.timeit(stmt='search.loop()', setup=setup, number = 90000000)
        list_comprehension_time = timeit.timeit(stmt='search.list_comprehension()', setup=setup, number=90000000)
        map_time=timeit.timeit(stmt='search.search_map()', setup=setup, number=90000000)

        time = sorted([loop_time, list_comprehension_time, map_time])

        if list_comprehension_time <= loop_time and list_comprehension_time <= map_time:
            print("It is better to use a list comprehension")
        elif map_time <= loop_time and map_time <= list_comprehension_time:
            print("It is better to use a map")
        else:
            print("it is better to use a loop")

        #print(search.search_map())
        #print(search.loop())
        #print(search.list_comprehension())

        print(f"{time[0]} vs {time[1]} vs {time[2]}")

    except Exception as error:
        print(error)

