
// call a function when the page is loaded
var data
async function load() {
   
    // get the data from the server
    await fetch('../bets/data.json',{mode: 'no-cors'}).then(
        res =>{res.text().then(res=>{
            data = res ? JSON.parse(res) : {}
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

function displayData(){
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
        sport.innerHTML = game.sport
        event_date.innerHTML = game.event_date
        bookmaker1.innerHTML = game.bookmaker1
        outcome1.innerHTML = game.outcome1
        odds1.innerHTML = game.odds1
        bookmaker2.innerHTML = game.bookmaker2
        outcome2.innerHTML = game.outcome2
        odds2.innerHTML = game.odds2
        profit.innerHTML = game.profit +"%"

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