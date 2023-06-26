

#import json file
import json
import requests
import json
import time
from datetime import datetime    
api_key = json.load(open('info.json'))['key']
testJson = json.load(open('./bets/response.json'))

def getMatchbookURL(outcome1,outcome2):
    searchUrl = "https://www.matchbook.com/beta/api/search?language=en&limit=500&offset=0&query="+outcome1+"%20"+outcome2
    data = get_json(searchUrl)
    if data=="error":
        return "error"
    else:
      
        id= data['results'][0]['id']
        sport = data['results'][0]['categories'][2]['url-name']
        event = data['results'][0]['categories'][3]['url-name']
        return  "https://www.matchbook.com/events/"+sport+"/"+event+"/"+str(id)

def getWillianUrl(outcome1, outcome2):   
    searchUrl = "https://search.williamhill.com/v2/?locale=en-gb&q="+outcome1+"%20"+outcome2+"&type=match" 
    data = get_json(searchUrl)
    if data == "error":
        print("error")
    else:
        id = data["data"]["hits"][0]["value"]["id"]
        sport = data["data"]["hits"][0]["value"]["sport"]["slug"]
        return "https://sports.williamhill.com/betting/en-gb/"+sport+"/"+id
    
def calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake):
    profit = ((back_odds - 1) * back_stake) - ((lay_odds - 1) * lay_stake)
    profit = round(profit, 2)
    return profit

def calculate_liability(back_odds, back_stake, lay_odds):
    liability = (back_stake * (back_odds - 0.02)) / (lay_odds - 0.02)
    return liability

def calculate_lay_stake(back_odds, back_stake, lay_odds):
    lay_stake = (back_stake * (back_odds )) / (lay_odds - 0.02)
    return round(lay_stake, 2)

def isArbitrageBookExchange(back_odds, back_stake, lay_odds):
    
    #if (back_odds - 1) * back_stake > (lay_odds - 1) * calculate_lay_stake(back_odds, back_stake, lay_odds):
    if (back_odds * back_stake -(lay_odds * calculate_lay_stake(back_odds, back_stake, lay_odds)) > 0):
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
    if response.status_code != 200:
        return "error"
    else:
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

sportURL = "https://api.the-odds-api.com/v4/sports/?apiKey="+api_key

def FindArbs():

    exclude = ["1xBet","MyBookie.ag","Pinnacle"]
    subscribed = ["matchbook","paddypower","bet365","betfair","betfairExchange","nordicbet","leovegas","williamhill"]
    print("(+) info: Getting json from api")
    
    url = "https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey="+api_key+"&regions=eu,uk&markets=h2h&oddsFormat=decimal&dateFormat=unix"
    print("(+) url: "+url)
    response = get_json(url)
    #response = testJson
    #save the json file
    
    with open('./bets/response.json', 'w') as file:
        print("(+) info: Saving response.json file")
        json.dump(response, file)
    print("(+) info: file saved")

    with open('./bets/data.json', 'w') as outfile:
        outfile.write('{') # start of object
        outfile.write('"bets":[') # start of array
    first = True # boolean to check if it is the first object in the array
    bookmakers = []
    sports = []

    
    for sport in response:#loop through sports
        print("(+) info: Sport: "+str(sport['sport_key'])) # type: ignore
        
        for i,bookmaker in enumerate(sport["bookmakers"]): #loop through bookmakers # type: ignore
            if bookmaker['title'] in exclude:  # type: ignore
                #print("(+) info: Bookmaker "+str(bookmaker['title'])+" is not trusted")
                continue
            referenceBookmaker = bookmaker #get the bookmaker object

            for j,referenceMarket in enumerate(referenceBookmaker['markets']): #loop through the markets of the reference bookmaker   
                for k,nextBookmaker in enumerate(sport["bookmakers"],i+1): #loop through the rest of the bookmakers
                    if nextBookmaker['title'] in exclude:
                        #print("(+) info: Bookmaker "+str(nextBookmaker['key'])+" is not trusted")
                        continue
    
                    for l,nextMarket in enumerate(nextBookmaker['markets']): #loop through the markets of the next bookmaker
                        referenceOutcomes = referenceMarket['outcomes'] #get the outcomes of the reference bookmaker
                        legs = len(referenceOutcomes)
                        
                        #if len(nextBookmaker['markets'])<2:
                        #    continue
                        nextOutcomes = nextMarket['outcomes'] # type: ignore #get the outcomes of the next bookmaker
                        netxtLEGS = len(nextOutcomes)
                        for n,referenceOutcome in enumerate(referenceOutcomes): #loop through the outcomes of the reference bookmaker

                            for o,nextOutcome in enumerate(nextOutcomes): #loop through the outcomes of the next bookmaker
                                #print("reference outcome: "+str(referenceOutcome['name'])+" next outcome: "+str(nextOutcome['name']))
                                layods = 0
                                backods = 0

                                if nextMarket['key']=="h2h" and referenceMarket['key']=="h2h" and (legs > 2 or netxtLEGS > 2):
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
                                    backods = referenceOutcome['price'] # type: ignore
                                    bookmaker1Type = "bookmaker"
                                else:
                                    layods = referenceOutcome['price']
                                    bookmaker1Type = "exchange" 
                                    
                                arbFound = False
                                profit= 0
                                outcome_check=False 
                                if nextMarket['key']=="h2h" and referenceMarket['key']=="h2h":
                                    arbFound = isArbitrageBookBook(referenceOutcome['price'],100,nextOutcome['price']) # type: ignore
                                    if arbFound:
                                        if referenceOutcome['name'] != nextOutcome['name']:
                                            outcome_check = True
                                        #print("arb found: "+str(arbFound)+ " bookemakers "+str(outcome_check))
                                        profit = calculate_profitBookBook(referenceOutcome['price'],100,nextOutcome['price'])
                                else:

                                    arbFound = isArbitrageBookExchange(backods,100,layods)
                                    if arbFound:
                                        if referenceOutcome['name'] == nextOutcome['name']: # type: ignore
                                            outcome_check = True
                                        #print("arb found: "+str(arbFound)+ " mixed "+str(outcome_check))
                                        profit = calculate_profitBookExchange(backods,100,layods)
                                
                                if  arbFound and outcome_check and referenceBookmaker['title'] != nextBookmaker['title']:
                                    
                                    if referenceBookmaker['title'] not in bookmakers: # type: ignore
                                        bookmakers.append(referenceBookmaker['title'])
                                    if nextBookmaker['title'] not in bookmakers:
                                        bookmakers.append(nextBookmaker['title'])
                                    if sport['sport_title'] not in sports:
                                        sports.append(sport['sport_title'])
                                    
                                    matchbookUrl = ""
                                    willianHillUrl = ""
                                    paddyPowerUrl = ""

                                    if referenceBookmaker['title'] == "Matchbook" or nextBookmaker['title'] == "Matchbook":
                                        matchbookUrl = getMatchbookURL(referenceOutcome['name'],nextOutcome['name'])

                                    if referenceBookmaker['title'] == "William Hill" or nextBookmaker['title'] == "William Hill":
                                        willianHillUrl = getWillianUrl(referenceOutcome['name'],nextOutcome['name'])

                                    active = ["Matchbook","William Hill","Paddy Power"]                                           
                                    if referenceBookmaker['title'] in active and nextBookmaker['title'] in active :  
                                        if profit > 1:
                                            print("===============FOUND ARB====================")
                                    obj = {
                                        "sport": sport['sport_title'], # type: ignore
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
                                        "legs": legs,
                                        "matchbookUrl": matchbookUrl,
                                        "willianHillUrl": willianHillUrl,
                                        "paddyPowerUrl": paddyPowerUrl
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



#function start

while(True):
    FindArbs()
    time.sleep(300)
    
