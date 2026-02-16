import sys

# for index,i in enumerate(argument)

def processing_data(our):
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

    if our.capitalize() in COMPANIES:
        company = our.capitalize()
        print(f'{company} stock price is {STOCKS[COMPANIES[company]]}')
    elif our.upper() in STOCKS:
        stock = our.upper()
        new_companies = dict(zip(COMPANIES.values(), COMPANIES.keys()))
        print(f'{stock} is a ticker symbol for {new_companies[stock]}')
    else:
        print(f'{our} is an unknown company or an unknown ticker symbol')

def all_stocks():
    if len(sys.argv) != 2:
        return 1
    arg = sys.argv[1]

    if ',,' in arg.replace(' ', '').replace('\t', '').replace('\n', ''):
        return 1

    arg=arg.replace(' ', '')
    mas=arg.split(',')
    for i in mas:
        #if i:
        processing_data(i)

if __name__ == '__main__':
    all_stocks()