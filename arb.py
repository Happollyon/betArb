

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

def isArbitrageBookExchange(back_odds, back_stake, lay_odds):
    if (back_odds - 1) * back_stake > (lay_odds - 1) * calculate_lay_stake(back_odds, back_stake, lay_odds):
        return True
    else:
        return False
    
def isArbitrageBookBook(back_odds, back_stake, lay_odds):
    if 1/back_odds + 1/lay_odds < 1:
        return True
    else:
        return False
    
def calculate_profitBookExchange(back_odds, back_stake, lay_odds):
    if isArbitrageBookExchange(back_odds, back_stake, lay_odds):
        lay_stake = calculate_lay_stake(back_odds, back_stake, lay_odds)
        profit = calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake)

        return round((profit * 100 )/(back_stake +lay_stake),2)
    else:
        return 0
def calculate_profitBookBook(back_odds, back_stake, lay_odds):
    return round((1-(1/back_odds + 1/lay_odds))*100,2)

#function that calls the api and returns the json
def get_json(url):
    response = requests.get(url)
    return response.json()


#function that creates converts unix time to readable time format ireland
def unix_to_time(unix_time):   
    readable = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    return readable

# functions that takes odds and returns the profit
def profit(odd1,odd2):
    cal = (1/odd1)+(1/odd2)
    return round((1-cal)*100,2)

#this request costs 2   credits
url = "https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey="+api_key+"&regions=eu,uk&markets=h2h&oddsFormat=decimal&dateFormat=unix"



def FindArbs():
    notTrustedBookmakers = ["1xBet","MyBookie.ag"]
    print("(+) info: Getting json from api")
    response = get_json(url)
    #response = testJson
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
            if bookmaker['title'] in notTrustedBookmakers: 
                #print("(+) info: Bookmaker "+str(bookmaker['title'])+" is not trusted")
                continue
            referenceBookmaker = bookmaker #get the bookmaker object

            for j,referenceMarket in enumerate(referenceBookmaker['markets']): #loop through the markets of the reference bookmaker   
                for k,nextBookmaker in enumerate(sport["bookmakers"],i+1): #loop through the rest of the bookmakers
                    if nextBookmaker['title'] in notTrustedBookmakers:
                        #print("(+) info: Bookmaker "+str(nextBookmaker['key'])+" is not trusted")
                        continue
    
                    for l,nextMarket in enumerate(nextBookmaker['markets']): #loop through the markets of the next bookmaker
                        referenceOutcomes = referenceMarket['outcomes'] #get the outcomes of the reference bookmaker
                        legs = len(referenceOutcomes)
                        #if len(nextBookmaker['markets'])<2:
                        #    continue
                        nextOutcomes = nextMarket['outcomes'] #get the outcomes of the next bookmaker

                        for n,referenceOutcome in enumerate(referenceOutcomes): #loop through the outcomes of the reference bookmaker

                            for o,nextOutcome in enumerate(nextOutcomes): #loop through the outcomes of the next bookmaker
                                #print("reference outcome: "+str(referenceOutcome['name'])+" next outcome: "+str(nextOutcome['name']))
                                layods = 0
                                backods = 0

                                if nextMarket['key']=="h2h" and referenceMarket['key']=="h2h" and legs > 2:
                                    continue
                                if nextMarket['key']=="h2h_lay" and referenceMarket['key']=="h2h_lay":
                                    continue
                                if nextMarket['key']=="h2h":
                                    backods = nextOutcome['price']
                                    bookmaker2Type = "bookmaker"
                                else:
                                    layods = nextOutcome['price']
                                    bookmaker2Type = "exchange"
                                if referenceMarket['key']=="h2h":
                                    backods = referenceOutcome['price']
                                    bookmaker1Type = "bookmaker"
                                else:
                                    layods = referenceOutcome['price']
                                    bookmaker1Type = "exchange" 
                                      
                                arbFound = False
                                profit= 0
                                outcome_check=False 
                                if nextMarket['key']=="h2h" and referenceMarket['key']=="h2h":
                                    arbFound = isArbitrageBookBook(referenceOutcome['price'],100,nextOutcome['price'])
                                    if arbFound:
                                        if referenceOutcome['name'] != nextOutcome['name']:
                                            outcome_check = True
                                        #print("arb found: "+str(arbFound)+ " bookemakers "+str(outcome_check))
                                        profit = calculate_profitBookBook(referenceOutcome['price'],100,nextOutcome['price'])
                                else:

                                    arbFound = isArbitrageBookExchange(backods,100,layods)
                                    if arbFound:
                                        if referenceOutcome['name'] == nextOutcome['name']:
                                            outcome_check = True
                                        #print("arb found: "+str(arbFound)+ " mixed "+str(outcome_check))
                                        profit = calculate_profitBookExchange(backods,100,layods)
                                
                                if  arbFound and outcome_check and referenceBookmaker['title'] != nextBookmaker['title']:
                                    
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
                                        "bookmaker1Type": bookmaker1Type,
                                        "outcome1": referenceOutcome['name'],
                                        "odds1": referenceOutcome['price'],
                                        "bookmaker2": nextBookmaker['title'],
                                        "bookmaker2Type": bookmaker2Type,
                                        "outcome2": nextOutcome['name'],
                                        "odds2": nextOutcome['price'],
                                        "profit": profit,
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