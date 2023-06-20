
// call a function when the page is loaded
var data
var backupData
async function load() {
   
    // get the data from the server
    await fetch('../bets/data.json',{mode: 'no-cors'}).then(
        res =>{res.text().then(res=>{
            data = res ? JSON.parse(res) : {}
            backupData = data
            displayData()
            loadSportOtions()   
            loadBookmakerOtions()
            
        })}
        
    )
    
}
function sortData(key) {
    let sortType = document.querySelector('input[name="sortType"]:checked').value;
    
    if(sortType =="increasing"){
        data['bets'].sort((a, b) => {
        if (a[key] < b[key]) {
            return -1;
        }
        if (a[key] > b[key]) {
            return 1;
        }
        return 0;
        });
    }else{
        data['bets'].sort((a, b) => {
            if (a[key] < b[key]) {
                return 1;
            }
            if (a[key] > b[key]) {
                return -1;
            }
            return 0;
            });
            
    }
    document.getElementById('pannel').innerHTML = ""
    displayData();
  }

function displayData(origin){
   let registered = ["Betfair","Betfair Sportsbook","William Hill","Paddy Power","Nordic Bet","LeoVegas","Matchbook"]
    document.getElementById('pannel').innerHTML = ""
     data['bets'].map((game) => {
        // create the elements
        var row = document.createElement('div')
        var innerRow1 = document.createElement('div')
        var innerRow2 = document.createElement('div')
        
        var sport = document.createElement('div')
        var event_date = document.createElement('div')
        var bookmaker1 = document.createElement('div')
        var outcome1 = document.createElement('div')
        var odds1 = document.createElement('div')
        var bookmaker2 = document.createElement('div')
        var outcome2 = document.createElement('div')
        var odds2 = document.createElement('div')
        var profit = document.createElement('div')

        if(registered.includes(game.bookmaker1)&&registered.includes(game.bookmaker2))
        {
            row.style.background="#00513A"
        }

        row.className = 'row'
        sport.className = 'col'
        row.setAttribute('data-sport',game.sport)
        row.setAttribute('data-bookmaker1',game.bookmaker1)
        row.setAttribute('data-bookmaker2',game.bookmaker2)
        row.setAttribute('data-outcome1',game.outcome1)
        row.setAttribute('data-outcome2',game.outcome2)
        row.setAttribute('data-odds1',game.odds1)
        row.setAttribute('data-odds2',game.odds2)
        row.setAttribute('data-bookmaker1Type',game.bookmaker1Type)
        row.setAttribute('data-bookmaker2Type',game.bookmaker2Type)
        row.setAttribute('data-matchbookUrl',game.matchbookUrl)
        row.setAttribute('data-willianHillUrl',game.willianHillUrl)
        event_date.className = 'col'
        bookmaker1.className = 'col'
        outcome1.className = 'col'
        outcome1.id = 'outcome1'
        odds1.className = 'col'
        bookmaker2.className = 'col'
        outcome2.className = 'col'
        outcome2.id = 'outcome2'
        odds2.className = 'col'
        profit.className = 'col'
        profit.id = 'profit'

        // set the content
        sport.innerHTML = "("+game.legs+") "+game.sport
        event_date.innerHTML = game.event_date
        bookmaker1.innerHTML = game.bookmaker1
        outcome1.innerHTML = game.outcome1
        odds1.innerHTML = game.odds1
        bookmaker2.innerHTML = game.bookmaker2
        outcome2.innerHTML = game.outcome2
        odds2.innerHTML = game.odds2
        profit.innerHTML = game.profit + "%"

        if(game.bookmaker1Type == "bookmaker"){
            outcome1.style.color = "green"
        }else{
            outcome1.style.color = "red"
        }
        if(game.bookmaker2Type == "bookmaker"){
            outcome2.style.color = "green"
        
        }else{
            outcome2.style.color = "red"
        }

        innerRow1.appendChild(bookmaker1)
        innerRow1.appendChild(outcome1)
        innerRow1.appendChild(odds1)
        innerRow2.appendChild(bookmaker2)
        innerRow2.appendChild(outcome2)
        innerRow2.appendChild(odds2)

        // add the elements to the page
        row.appendChild(sport)
        row.appendChild(event_date)
        row.appendChild(innerRow1)
        row.appendChild(innerRow2)
        row.appendChild(profit)
        row.addEventListener('click', ()=>OpenBet(this.event))
        document.getElementById('pannel').appendChild(row)
    })}


function loadSportOtions(){
    data['sports'].map((sport) => {
        var option = document.createElement('option')
        option.value = sport
        option.innerHTML = sport
        document.getElementById('selectSport').appendChild(option)
    })
}
async function filterDataBySport(){
    data['bets'] = await data['bets'].filter((game) => {
        
        return game.sport == document.getElementById('selectSport').value
    })
    console.log(data)
    displayData()
}

function loadBookmakerOtions(){
   
    data['bookmakers'].map((bookmaker) => {
        var option1 = document.createElement('option')
        var option2 = document.createElement('option')
        option1.value = bookmaker
        option1.innerHTML = bookmaker
        option2.value = bookmaker
        option2.innerHTML = bookmaker
        document.getElementById('selectBookmaker1').appendChild(option1)
        document.getElementById('selectBookmaker2').appendChild(option2)
    })
}

function filterBookemakerPairs(){


    let bookmaker1 = document.getElementById('selectBookmaker1').value
    let bookmaker2 = document.getElementById('selectBookmaker2').value
    data['bets'] = data['bets'].filter((game) => {
        return (game.bookmaker1 == bookmaker1 || game.bookmaker1== bookmaker2 )&& (game.bookmaker2 == bookmaker2 || game.bookmaker2 == bookmaker1)  
        
    })
    
    displayData()
}
function OpenBet(event){
    let url1
    let url2 
    
    //["Betfair","Betfair Sportsbook","William Hill","Paddy Power","Nordic Bet","LeoVegas","Matchbook"]
    alert(event.target.getAttribute('data-bookmaker1'))
    switch(event.target.getAttribute('data-bookmaker1')){
        
        case "Paddy Power":
            url1 = "https://www.paddypower.com/search?q="+event.target.getAttribute('data-outcome1')+"%20v%20"+event.target.getAttribute('data-outcome2')
            break;
        case "Matchbook":
            url1 = event.target.getAttribute('data-matchbookUrl')
            break;
        case "William Hill":
            url1 =event.target.getAttribute('data-willianHillUrl')
            break;
        case "LeoVegas":
            url1 ="https://www.leovegas.com/en-row/betting#home"
            break;
         }
    switch(event.target.getAttribute('data-bookmaker2')){
        case "Paddy Power":
            url2 =  "https://www.paddypower.com/search?q="+event.target.getAttribute('data-outcome1')+"%20v%20"+event.target.getAttribute('data-outcome2')
            break;
        case "Matchbook":
            url2 = event.target.getAttribute('data-matchbookUrl')
            break;
        case "William Hill":
            url2 =event.target.getAttribute('data-willianHillUrl')
            break;
        case "LeoVegas":
            url2 ="https://www.leovegas.com/en-row/betting#home"
            break;
        }
    
    let row = event.target
    if(row.getAttribute('data-bookmaker1Type') == "bookmaker" && row.getAttribute('data-bookmaker2Type') == "bookmaker"){
        document.getElementById('betting-panel').style.display = 'flex'
        document.getElementById('betting-bookmaker1').addEventListener('click', function() {
            window.open(url1, '_blank');
          });
         
        document.getElementById('betting-bookmaker2').addEventListener('click', function() {
            window.open(url2, '_blank');
        });
        document.getElementById('betting-sport').innerHTML = "Sport: "+row.getAttribute('data-sport')
        document.getElementById('betting-bookmaker1').innerHTML = "bookmaker1: "+row.getAttribute('data-bookmaker1')
        document.getElementById('betting-outcome1').innerHTML = "team 1: "+row.getAttribute('data-outcome1')
        document.getElementById('betting-odds1').innerHTML = "bookmaker1 odds: " + row.getAttribute('data-odds1')
        document.getElementById('betting-bookmaker2').innerHTML = "Bookmaker2: "+row.getAttribute('data-bookmaker2')
        document.getElementById('betting-outcome2').innerHTML = "team 2: " + row.getAttribute('data-outcome2')
        document.getElementById('betting-odds2').innerHTML = "bookmaker2 odds:  "+row.getAttribute('data-odds2')
        document.getElementById("calculateBtn").addEventListener('click',()=>calculateBet(row))
        document.getElementById('profit-bookmaker').innerHTML = "Bookmaker1 profit: €0,00"
        document.getElementById('profit-exchange').innerHTML = "Bookmaker2 profit: €0,00 "
        document.getElementById('lay-stake').innerHTML = "bookmaker1 stake: €0,00 "
        document.getElementById('back-stake').innerHTML = "bookmaker2 stake: €0,00" 
    }else{
        if(
            row.getAttribute('data-bookmaker1Type')=="bookmaker"){
            document.getElementById('betting-panel').style.display = 'flex'
            document.getElementById('betting-panel').style.display = 'flex'
            document.getElementById('betting-sport').innerHTML = "Sport: "+row.getAttribute('data-sport')
            document.getElementById('betting-bookmaker1').innerHTML = "bookmaker: "+row.getAttribute('data-bookmaker1')
            document.getElementById('betting-bookmaker1').addEventListener('click', function() {
                window.open(url1, '_blank');
              });
             
            document.getElementById('betting-bookmaker2').addEventListener('click', function() {
                window.open(url2, '_blank');
            });
            document.getElementById('betting-outcome1').innerHTML = "back team : "+row.getAttribute('data-outcome1')
            document.getElementById('betting-odds1').innerHTML = "bookmaker odds: " + row.getAttribute('data-odds1')
            document.getElementById('betting-bookmaker2').innerHTML = "exchange: "+row.getAttribute('data-bookmaker2')
            document.getElementById('betting-outcome2').innerHTML = "lay team : " + row.getAttribute('data-outcome2')
            document.getElementById('betting-odds2').innerHTML = "exchange odds:  "+row.getAttribute('data-odds2')
            document.getElementById("calculateBtn").addEventListener('click',()=>calculateBet(row))
            document.getElementById('profit-bookmaker').innerHTML = "Bookmaker profit: €0,00"
            document.getElementById('profit-exchange').innerHTML = "exchange profit: €0,00 "
            document.getElementById('lay-stake').innerHTML = "exchange stake: €0,00 "
            document.getElementById('back-stake').innerHTML = "Bookmaker stake: €0,00" 
        }else{
            document.getElementById('betting-bookmaker1').addEventListener('click', function() {
                window.open(url1, '_blank');
              });
             
            document.getElementById('betting-bookmaker2').addEventListener('click', function() {
                window.open(url2, '_blank');
            });
            document.getElementById('betting-panel').style.display = 'flex'
            document.getElementById('betting-sport').innerHTML = "Sport: "+row.getAttribute('data-sport')
            document.getElementById('betting-bookmaker1').innerHTML = "Exchange: "+row.getAttribute('data-bookmaker1')
            document.getElementById('betting-outcome1').innerHTML = "Lay team : "+row.getAttribute('data-outcome1')
            document.getElementById('betting-odds1').innerHTML = "Exchange odds: " + row.getAttribute('data-odds1')
            document.getElementById('betting-bookmaker2').innerHTML = "Bookmaker: "+row.getAttribute('data-bookmaker2')
            document.getElementById('betting-outcome2').innerHTML = "Back team : " + row.getAttribute('data-outcome2')
            document.getElementById('betting-odds2').innerHTML = "Bookmaker odds:  "+row.getAttribute('data-odds2')
            document.getElementById("calculateBtn").addEventListener('click',()=>calculateBet(row))
            document.getElementById('profit-bookmaker').innerHTML = "Exchange profit: €0,00"
            document.getElementById('profit-exchange').innerHTML = "Bookmaker profit: €0,00 "
            document.getElementById('lay-stake').innerHTML = "Bookmaker stake: €0,00 "
            document.getElementById('back-stake').innerHTML = "Exchange stake: €0,00" 
        }

    }

}
function calculateBet(row){
    
    // identify if its mixed or bookmaker only
        // calulate accoringly
        // display accordingly

    // identify which is the bookmaker and which is the exchange
        // calculate accoringly
        // display accordingly
    if(row.getAttribute('data-bookmaker1Type') == "bookmaker" && row.getAttribute('data-bookmaker2Type') == "bookmaker"){
        
        let back_stake = document.getElementById('backStake').value
        let bookmaker1Odds = row.getAttribute('data-odds1')
        let bookmaker2Odds = row.getAttribute('data-odds2')

        //Rafael Nadal stake = (£500 x 84.746%) / 99.032% = £427.87
        //Kyle Edmund stake = (£500 x 14.286%) / 99.032% = £72.13
        //£427.87 + £72.13 = £500 total stake
        
        let bookmaker1Stake = (back_stake * (1/bookmaker1Odds)) / (1/bookmaker1Odds + 1/bookmaker2Odds)
        let bookmaker2Stake = (back_stake * (1/bookmaker2Odds)) / (1/bookmaker1Odds+ 1/bookmaker2Odds)
        let bookmaker1Profit = (bookmaker1Stake * bookmaker1Odds) - (bookmaker1Stake + bookmaker2Stake)
        let bookmaker2Profit = (bookmaker2Stake * bookmaker2Odds) - (bookmaker1Stake + bookmaker2Stake)
        bookmaker1Profit = Math.round(bookmaker1Profit)
        bookmaker2Profit = Math.round(bookmaker2Profit)
        
        document.getElementById('back-stake').innerHTML = "bookmaker1 stake: €"+ bookmaker1Stake
        document.getElementById('lay-stake').innerHTML = "bookmaker2 stake: €"+ bookmaker2Stake
        document.getElementById('profit-bookmaker').innerHTML = "bookmaker1 profit: €"+ bookmaker1Profit
        document.getElementById('profit-exchange').innerHTML = "bookmaker2 profit: €"+ bookmaker2Profit


    }else {
        let lay_odds
        let back_odds
        if(row.getAttribute('data-bookmaker1Type') == "bookmaker"){
            back_odds = row.getAttribute('data-odds1')
            lay_odds = row.getAttribute('data-odds2')
            let back_stake = document.getElementById('backStake').value
        
            let lay_stake = calculate_lay_stake(back_odds, back_stake, lay_odds)
            let exchangeProfit = calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake)
            let bookmakerProfit = calculate_bookmaker_profit(back_odds, back_stake, lay_odds, lay_stake)
            alert("lay stake: "+ lay_stake + " exchange profit: "+ exchangeProfit + " bookmaker profit: "+ bookmakerProfit)
            document.getElementById('profit-bookmaker').innerHTML = "Bookmaker profit: €"+ bookmakerProfit
            document.getElementById('profit-exchange').innerHTML = "exchange profit: €"+ exchangeProfit
            document.getElementById('lay-stake').innerHTML = "Lay stake: €"+ lay_stake
            document.getElementById('back-stake').innerHTML = "back stake: €" + back_stake
        }else{
            back_odds = row.getAttribute('data-odds2')
            lay_odds = row.getAttribute('data-odds1')
        
            let back_stake = document.getElementById('backStake').value
        
            let lay_stake = calculate_lay_stake(back_odds, back_stake, lay_odds)
            let exchangeProfit = calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake)
            let bookmakerProfit = calculate_bookmaker_profit(back_odds, back_stake, lay_odds, lay_stake)
            
            document.getElementById('profit-bookmaker').innerHTML = "exchange profit: €"+ exchangeProfit
            document.getElementById('profit-exchange').innerHTML = "bookmaker profit: €"+ bookmakerProfit
            document.getElementById('lay-stake').innerHTML = "back stake: €"+ back_stake
            document.getElementById('back-stake').innerHTML = "lay stake: €" + lay_stake
        }

        
        
    }
}
function calculate_lay_stake(back_odds, back_stake, lay_odds) {
    let lay_stake = (back_stake * (back_odds - 0.02)) / (lay_odds - 0.02);
    return Math.round(lay_stake * 100) / 100;
}

function isArbitrage(back_odds, back_stake, lay_odds) {
    if ((back_odds - 1) * back_stake > (lay_odds - 1) * calculate_lay_stake(back_odds, back_stake, lay_odds)) {
        return true;
    } else {
        return false;
    }
}
function calculate_bookmaker_profit(back_odds, back_stake, lay_odds, lay_stake) {
    let profit = ((back_odds - 1) * back_stake) - ((lay_odds - 1) * lay_stake);
    profit = Math.round(profit * 100) / 100;
    return profit;
}

function calculate_profit(back_odds, back_stake, lay_odds) {
    if (isArbitrage(back_odds, back_stake, lay_odds)) {
        return calculate_exchange_profit(back_odds, back_stake, lay_odds, calculate_lay_stake(back_odds, back_stake, lay_odds));
    } else {
        return 0;
    }
}
function calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake) {
    let profit = ((back_odds - 1) * back_stake) - ((lay_odds - 1) * lay_stake);
    profit = Math.round(profit * 100) / 100;
    return profit;
}
function calculate_liability(back_odds, back_stake, lay_odds) {
    let liability = (back_stake * (back_odds - 0.02)) / (lay_odds - 0.02);
    return liability;
}