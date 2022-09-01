// show actors' birthday on click

const actors = document.querySelectorAll('p')
// console.log(actors)

for (let i=0; i<actors.length; i++){
    actors[i].addEventListener('click', async() => {
            // console.log(actors[i])
        const response = await fetch('/api/get-actor-year/$actors[i].innerHTML')
        const years = await response.json()
        // console.log(years)
        // let toDisplay = ''
        // for (let year in years){
        //     toDisplay =  `${toDisplay}<div>${year}</div>`
        // }
        // document.getElementById('result').innerHTML = toDisplay
    })
}

