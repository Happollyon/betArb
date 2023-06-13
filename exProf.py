def calculate_book_profit(back_odds, back_stake, lay_odds, lay_stake):
    profit = ((back_odds - 1) * back_stake) - ((lay_odds - 1) * lay_stake)
    profit = round(profit, 2)
    return profit
def calculate_exchange_profit( back_stake, lay_stake):
    profit = (lay_stake * (1 - 0.02)) - back_stake
    profit = round(profit, 2)
    return profit
def calculate_liability(back_odds, back_stake, lay_odds):
    liability = (back_stake * (back_odds - 0.02)) / (lay_odds - 0.02)
    return liability

def calculate_lay_stake(back_odds, back_stake, lay_odds):
    lay_stake = (back_stake * (back_odds - 0.02)) / (lay_odds - 0.02)
    return round(lay_stake, 2)

def isArbitrage(back_odds, back_stake, lay_odds):
    if (back_odds - 1) * back_stake > (lay_odds - 1) * calculate_lay_stake(back_odds, back_stake, lay_odds):
        return True
    else:
        return False
    
def calculate_profit(back_odds, back_stake, lay_odds):
    if isArbitrage(back_odds, back_stake, lay_odds):
        return calculate_exchange_profit(back_odds, back_stake, lay_odds, calculate_lay_stake(back_odds, back_stake, lay_odds))
    else:
        return 0

back_odds = 2.2
back_stake = 200
lay_odds = 1.98
lay_stake = calculate_lay_stake(back_odds, back_stake, lay_odds)
profit = calculate_book_profit(back_odds, back_stake, lay_odds, lay_stake)
liability = calculate_liability(back_odds, back_stake, lay_odds)

print("isArbitrage: " + str(isArbitrage(back_odds, back_stake, lay_odds)))
print("lay stake: " + str(lay_stake))
print("profit book: " + str(profit))
print("profit exchange: " + str(calculate_exchange_profit(back_stake, lay_stake)))
print("liability: " + str(liability))