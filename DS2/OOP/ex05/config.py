import sys

num_of_steps=3
FILE_NAME=sys.argv[1]
NEW_FILE="report"
EXTENSION="txt"


TEMPLATE_REPORT='''Report:

We made {number} observations by tossing a coin: {number_of_tails} were tails and {number_of_heads} were heads. 
The probabilities are {percent_of_tails:.2f}% and {percent_of_heads:.2f}%, respectively. 
Our forecast is that the next {num_of_steps} observations will be: {random_tails} tail and {random_heads} heads.'''
