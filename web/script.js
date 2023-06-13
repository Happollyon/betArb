
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

        row.className = 'row'
        sport.className = 'col'
        row.setAttribute('data-sport',game.sport)
        row.setAttribute('data-bookmaker1',game.bookmaker1)
        row.setAttribute('data-bookmaker2',game.bookmaker2)
        row.setAttribute('data-outcome1',game.outcome1)
        row.setAttribute('data-outcome2',game.outcome2)
        row.setAttribute('data-odds1',game.odds1)
        row.setAttribute('data-odds2',game.odds2)
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
        profit.innerHTML = game.profit

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
    let row = event.target
    document.getElementById('betting-panel').style.display = 'flex'
    document.getElementById('betting-sport').innerHTML = "Sport: "+row.getAttribute('data-sport')
    document.getElementById('betting-bookmaker1').innerHTML = "bookmaker: "+row.getAttribute('data-bookmaker1')
    document.getElementById('betting-outcome1').innerHTML = "back team: "+row.getAttribute('data-outcome1')
    document.getElementById('betting-odds1').innerHTML = "bookmaker odds: " + row.getAttribute('data-odds1')
    document.getElementById('betting-bookmaker2').innerHTML = "exchange: "+row.getAttribute('data-bookmaker2')
    document.getElementById('betting-outcome2').innerHTML = "lay team: " + row.getAttribute('data-outcome2')
    document.getElementById('betting-odds2').innerHTML = "layd odds:  "+row.getAttribute('data-odds2')
    document.getElementById("calculateBtn").addEventListener('click',()=>calculateBet(row))


}
function calculateBet(row){
    
    let back_odds = row.getAttribute('data-odds1')
    let back_stake = document.getElementById('backStake').value
    let lay_odds = row.getAttribute('data-odds2')
    let lay_stake = calculate_lay_stake(back_odds, back_stake, lay_odds)
    let exchangeProfit = calculate_exchange_profit(back_odds, back_stake, lay_odds, lay_stake)
    let bookmakerProfit = calculate_bookmaker_profit(back_odds, back_stake, lay_odds, lay_stake)
    alert("lay stake: "+ lay_stake + " exchange profit: "+ exchangeProfit + " bookmaker profit: "+ bookmakerProfit)
    document.getElementById('profit-bookmaker').innerHTML = "Bookmaker profit: "+ bookmakerProfit
    document.getElementById('profit-exchange').innerHTML = "exchange profit: "+ exchangeProfit
    document.getElementById('lay-stake').innerHTML = "Lay stake: "+ lay_stake
    document.getElementById('back-stake').innerHTML = "back stake: " + back_stake
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