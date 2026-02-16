import sys

def output_name_and_price():
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

    if argument in STOCKS:
        price = STOCKS[argument]
        for key, value in COMPANIES.items():
            if value == argument:
                name = key
        print(f'{name} {price}')
    else:
        print("Unknown ticker")

if __name__ == '__main__':
    output_name_and_price()
