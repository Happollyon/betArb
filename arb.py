

#import json file
import json
import requests
import json
from datetime import datetime    
api_key = json.load(open('info.json'))['key']
testJson = json.load(open('test.json'))

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

print(unix_to_time(1686130200))
print(url)


def FindArbs():
    with open('./bets/data.json', 'w') as outfile:
        outfile.write('[') # start of array
    first = True # boolean to check if it is the first object in the array
    bookmakers = []
    for sport in testJson:#loop through sports

        for i,bookmaker in enumerate(sport["bookmakers"]): #loop through bookmakers
            homeTeam = sport['home_team'] #get the home team
            awayTeam = sport['away_team'] #get the away team
            referenceBookmaker = bookmaker #get the bookmaker object

            for j,nextBookmaker in enumerate(sport["bookmakers"],i+1): #loop through the rest of the bookmakers
                referenceOutcome = referenceBookmaker['markets'][0]['outcomes'] #get the outcomes of the reference bookmaker
                nextOutcome = nextBookmaker['markets'][0]['outcomes'] #get the outcomes of the next bookmaker

                for k in range(len(referenceOutcome)): #loop through the outcomes of the reference bookmaker

                    for l in range(len(nextOutcome)): #loop through the outcomes of the next bookmaker
                        if arb(referenceOutcome[k]['price'],nextOutcome[l]['price']) and referenceOutcome[k]['name'] != nextOutcome[l]['name'] and referenceBookmaker['title'] != nextBookmaker['title']:
                            
                            print("sport: " + sport['sport_title'])
                            print("date: " + unix_to_time(sport['commence_time']))
                            print("bookmaker1: " + referenceBookmaker['title'] + " -> " + referenceOutcome[k]['name']+ " -> " + str(referenceOutcome[k]['price']))
                            print("bookmaker2: " + nextBookmaker['title'] + " -> " + nextOutcome[l]['name']+ " -> " + str(nextOutcome[l]['price']))
                            #  bookmaker1: Bet365 -> australia to win -> 1.5
                            #  bookmaker2: Betfair -> india to win -> 1.6
                            print("profit: " + str(profit(referenceOutcome[k]['price'],nextOutcome[l]['price'])) + "%")
                            print("")
                            if referenceBookmaker['title'] not in bookmakers:
                                bookmakers.append(referenceBookmaker['title'])
                            if nextBookmaker['title'] not in bookmakers:
                                bookmakers.append(nextBookmaker['title'])
                            obj = {
                                "sport": sport['sport_title'],
                                "event_date": unix_to_time(sport['commence_time']),
                                "bookmaker1": referenceBookmaker['title'],
                                "outcome1": referenceOutcome[k]['name'],
                                "odds1": referenceOutcome[k]['price'],
                                "bookmaker2": nextBookmaker['title'],
                                "outcome2": nextOutcome[l]['name'],
                                "odds2": nextOutcome[l]['price'],
                                "profit": profit(referenceOutcome[k]['price'],nextOutcome[l]['price'])
                            }
                            with open('./bets/data.json', 'a') as outfile:
                                if not first:
                                    outfile.write(',')
                                json.dump(obj, outfile)
                                first = False
    with open('./bets/data.json', 'a') as outfile:
        outfile.write(']') # end of array                            
        
        json.dump(bookmakers, outfile)

FindArbs()