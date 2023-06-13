

#import json file
import json
import requests
import json
from datetime import datetime    
api_key = json.load(open('info.json'))['key']
testJson = json.load(open('./bets/response.json'))

def calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake):
    profit = ((back_odds - 1) * back_stake) - ((lay_odds - 1) * lay_stake)
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

#function that calls the api and returns the json
def get_json(url):
    response = requests.get(url)
    return response.json()


#function that creates converts unix time to readable time format ireland
def unix_to_time(unix_time):   
    readable = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    return readable

#function that takes odds and returns if there is an arb
def arb(odd1,odd2):
    cal = (1/odd1)+(1/odd2)
    if cal < 1:
        return True
    else:
        return False
# functions that takes odds and returns the profit
def profit(odd1,odd2):
    cal = (1/odd1)+(1/odd2)
    return round((1-cal)*100,2)

#this request costs 2   credits
url = "https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey="+api_key+"&regions=eu,uk&markets=h2h&oddsFormat=decimal&dateFormat=unix"



def FindArbs():
    print("(+) info: Getting json from api")
    response = get_json(url)
    #save the json file
    with open('./bets/response.json', 'w') as file:
        print("(+) info: Saving json file")
        json.dump(response, file)
    print("(+) info: file saved")

    with open('./bets/data.json', 'w') as outfile:
        outfile.write('{') # start of object
        outfile.write('"bets":[') # start of array
    first = True # boolean to check if it is the first object in the array
    bookmakers = []
    sports = []
    for sport in response:#loop through sports
        print("(+) info: Checking sport: "+str(sport['sport_title']))

        for i,bookmaker in enumerate(sport["bookmakers"]): #loop through bookmakers
            homeTeam = sport['home_team'] #get the home team
            awayTeam = sport['away_team'] #get the away team
            referenceBookmaker = bookmaker #get the bookmaker object

            for j,nextBookmaker in enumerate(sport["bookmakers"],i+1): #loop through the rest of the bookmakers
                referenceOutcome = referenceBookmaker['markets'][0]['outcomes'] #get the outcomes of the reference bookmaker
                legs = len(referenceOutcome)
                if len(nextBookmaker['markets'])<2:
                    continue
                nextOutcome = nextBookmaker['markets'][1]['outcomes'] #get the outcomes of the next bookmaker

                for k in range(len(referenceOutcome)): #loop through the outcomes of the reference bookmaker

                    for l in range(len(nextOutcome)): #loop through the outcomes of the next bookmaker
                        if isArbitrage(referenceOutcome[k]['price'],100,nextOutcome[l]['price']) and referenceOutcome[k]['name'] == nextOutcome[l]['name'] and referenceBookmaker['title'] != nextBookmaker['title']:
                            
                            if referenceBookmaker['title'] not in bookmakers:
                                bookmakers.append(referenceBookmaker['title'])
                            if nextBookmaker['title'] not in bookmakers:
                                bookmakers.append(nextBookmaker['title'])
                            if sport['sport_title'] not in sports:
                                sports.append(sport['sport_title'])
                            obj = {
                                "sport": sport['sport_title'],
                                "event_date": unix_to_time(sport['commence_time']),
                                "bookmaker1": referenceBookmaker['title'],
                                "outcome1": referenceOutcome[k]['name'],
                                "odds1": referenceOutcome[k]['price'],
                                "bookmaker2": nextBookmaker['title'],
                                "outcome2": nextOutcome[l]['name'],
                                "odds2": nextOutcome[l]['price'],
                                "profit": calculate_profit(referenceOutcome[k]['price'],100,nextOutcome[l]['price']),
                                "legs": legs
                            }
                            with open('./bets/data.json', 'a') as outfile:
                                if not first:
                                    outfile.write(',')
                                json.dump(obj, outfile)
                                first = False
    with open('./bets/data.json', 'a') as outfile:
        outfile.write('],"bookmakers":') # end of array                            
        
        json.dump(bookmakers, outfile)
        outfile.write(',"sports":') # end of array
        json.dump(sports, outfile)
        outfile.write('}') # end of object
    print("Done")

FindArbs()