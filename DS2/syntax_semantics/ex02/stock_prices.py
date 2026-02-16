import sys

def output_price():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }

    if len(sys.argv) != 2:
        return 1

    argument = sys.argv[1]

    #COMPANIES.keys()
    if argument in COMPANIES:
        stock = COMPANIES[argument]
        ans = STOCKS[stock]
        print(ans)
    else:
        print("Unknown company")

if __name__ == '__main__':
    output_price()


