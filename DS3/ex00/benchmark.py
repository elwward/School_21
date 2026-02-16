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


if __name__ == '__main__':
    try:

        setup = '''
from __main__ import Search
emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
search = Search(emails)
'''

        loop_time = timeit.timeit(stmt='search.loop()', setup=setup, number = 90000000)
        list_comprehension_time = timeit.timeit(stmt='search.list_comprehension()', setup=setup, number=90000000)

        if list_comprehension_time <= loop_time:
            print("It is better to use a list comprehension")
        else:
            print("it is better to use a loop")

        time = sorted([loop_time, list_comprehension_time])
        print(f"{time[0]} vs {time[1]}")

    except Exception as error:
        print(error)