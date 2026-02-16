import timeit
import sys

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
        return list(map(lambda i: i if i.endswith('@gmail.com') else None, self.emails))

    def search_filter(self):
        return list(filter(lambda i: i.endswith('@gmail.com'), self.emails))

    def choose(self,mode):
        if mode == "filter": return self.search_filter()
        elif mode == "map": return self.search_map()
        elif mode == "loop": return self.loop()
        elif mode == "list_comprehension": return self.list_comprehension()
        else: return None



if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit()

    try:

        setup = '''
from __main__ import Search
emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
search = Search(emails)
'''

        time = timeit.timeit(stmt=f'search.choose("{sys.argv[1]}")', setup=setup, number = int(sys.argv[2]))
        print(time)

    except Exception as error:
        print(error)



