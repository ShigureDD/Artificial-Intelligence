"""
Run python autograder.py 
"""


def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    avg = sum(set(priceList))/len(set(priceList))
    return avg
