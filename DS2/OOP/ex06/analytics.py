from random import randint
from config import *
import requests

class Research():
    def __init__(self, path):
        self.path = path
        logging.info("Initializing Research")

    def file_reader(self, has_header=True):
        with open(self.path, 'r') as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise ValueError("File is empty")

        if len(lines) == 1:
            raise ValueError("File does not contain enough lines")

        header = lines[0].strip().split(',')
        if len(header) != 2 or header != ['head', 'tail']:
            has_header = False

        if has_header:
            data=lines[1:]
        else:
            data=lines

        for line in data:
            if not line:
                raise ValueError("Empty line")
            parts = line.split(',')
            if len(parts) != 2:
                raise ValueError(f"Doesn't contain 2 columns")
            a, b = parts[0].strip(), parts[1].strip()
            if (a, b) != ('0', '1') and (a, b) != ('1', '0'):
                raise ValueError(f"Data is incorrect. Not 1,0 or 0,1")

        logging.info(f"Reading file {self.path}")
        return [list(map(int, i.strip().split(","))) for i in data]

    def telegram(self, status=True):
        if not TOKEN or not ID:
            logging.error("No token or id")
            print("No token or id")
            return

        webhook_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        if status:
            message = "The report has been successfully created"
        else: message = "The report hasn't been created due to an error"

        try:
            params = {
                'chat_id': ID,
                'text': message
            }
            requests.post(webhook_url, params=params)
            logging.info("Message was sent to Telegram")
        except Exception as error:
            logging.error(error)
            print(error)

    class Calculations:
        def __init__(self,data):
            self.data=data
            logging.info("Initializing Calculations")
        def counts(self):
            logging.info("Calculating the counts of heads and tails")
            return [sum([i[0] for i in self.data]), sum([i[1] for i in self.data])]
        def fractions(self, count):
            logging.info("Calculating the fractions of heads and tails")
            return [count[0]*100/(count[0]+count[1]), count[1]*100/(count[1]+count[0])]

class Analytics(Research.Calculations):
    def predict_random(self, number):
        result=[]
        for _ in range(number):
            first=randint(0,1)
            if first == 0:
                second=1
            else:
                second=0
            result.append([first, second])

        logging.info(f"Generating random predictions for {number} observations")
        return result

    def predict_last(self):
        logging.info("Returning the last item")
        return self.data[-1]

    def save_file(self, data, file_name, extension):
        with open(file_name + '.' + extension, 'w') as f:
            f.write(data)
        logging.info(f"Saved file {file_name}.{extension}")






