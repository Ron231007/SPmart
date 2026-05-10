import math


def calculateTotalPrice(items : list) -> float:
    sum = 0
    for item in items:
        sum += item[1] *item[2]

    return sum

#for every $10 spent, 30 points are earned. 100 points can be used to exchange for $5 discount
def calculatePoints(cost : float, isAdmin: bool) -> int:
    return math.floor(cost /10) * 60 if isAdmin else math.floor(cost / 10) *30



