import requests
import json

def get_json(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "error"
    else:
        return response.json()
    
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
    
def getWillianUrl(outcome1, outcome2):   
    searchUrl = "https://search.williamhill.com/v2/?locale=en-gb&q="+outcome1+"%20"+outcome2+"&type=match" 
    data = get_json(searchUrl)
    if data == "error":
        print("error")
    else:
        id = data["data"]["hits"][0]["value"]["id"]
        sport = data["data"]["hits"][0]["value"]["sport"]["slug"]
        return "https://sports.williamhill.com/betting/en-gb/"+sport+"/"+id


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
print("/n")

print(getWillianUrl("uruguay","cuba"))