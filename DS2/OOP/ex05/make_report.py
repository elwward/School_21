from analytics import *
from config import *

def main():
    if len(sys.argv) < 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    researcher=Research(FILE_NAME)
    data=researcher.file_reader()

    calculator = Research.Calculations(data)
    count=calculator.counts()
    fraction=calculator.fractions(count)

    analytics = Analytics(data)
    random_numbers=analytics.predict_random(num_of_steps)
    calculator_for_random = Research.Calculations(random_numbers)
    count_random = calculator_for_random.counts()

    report = TEMPLATE_REPORT.format(
        number=len(data),
        number_of_tails=count[0],
        number_of_heads=count[1],
        percent_of_tails=fraction[0],
        percent_of_heads=fraction[1],
        num_of_steps=num_of_steps,
        random_tails=count_random[0],
        random_heads=count_random[1],
    )

    analytics.save_file(report, NEW_FILE, EXTENSION)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)