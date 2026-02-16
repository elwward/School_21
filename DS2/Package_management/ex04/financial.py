import requests
import sys
from bs4 import BeautifulSoup
from time import sleep

#1 python -m cProfile -s tottime financial.py MSFT "Total Revenue" > profiling-sleep.txt
#2 python -m cProfile -s tottime financial.py MSFT "Total Revenue" > profiling-tottime.txt
#3 python -m cProfile -s tottime financial_enhanced.py MSFT "Total Revenue" > profiling-http.txt
#4 python -m cProfile -s ncalls financial_enhanced.py MSFT "Total Revenue" > profiling-ncalls.txt

class Parsing:
    def __init__(self, ticker, field):
        self.ticker = ticker.upper()
        self.field = field

    def information(self):
        url = f'https://finance.yahoo.com/quote/{self.ticker}/financials?p={self.ticker}'

        #429
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            raise Exception("Does not exist ticker")

        if response.status_code != 200 and response.status_code != 404:
            raise Exception(f'Site returned {response.status_code}')

        soup = BeautifulSoup(response.text, 'html.parser')

        # < div class ="row lv-0 yf-t22klz" > < div class ="column sticky yf-t22klz" >
        # < div class ="rowTitle yf-t22klz" title="Net Non Operating Interest Income Expense" >
        target = False
        for row in soup.find_all('div', class_='row lv-0 yf-t22klz'):
            title_div = row.find('div', class_='rowTitle yf-t22klz')
            if title_div and title_div.get('title') == self.field:
                target = row
                break

        if not target:
            raise Exception("Doesn't exist field")

        values = []
        for i in target.find_all('div', class_=['column yf-t22klz', 'column yf-t22klz alt']):
            if 'sticky' in i.get('class', []):
                continue
            value = i.get_text().strip()
            values.append(value)

        return (self.field,) + tuple(values[:5])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You need to enter the ticker and the table field.")
        exit()
    try:
        ticker = sys.argv[1]
        field= sys.argv[2].title()
        parser = Parsing(ticker, field)
        print(parser.information())

    except Exception as error:
        print(error)