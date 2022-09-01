// console.log('merge');

const allSeasons = document.querySelectorAll('p')
// console.log(allSeasons)
for (let i = 0; i<allSeasons.length; i++){
    // console.log(allSeasons[i])
    allSeasons[i].addEventListener('click', async () => {
        console.log(allSeasons[i])
        const response = await fetch(`/api/get-episodes/${allSeasons[i].innerHTML}`)
        const episodes = await response.json()
        // console.log(episodes)//error, no route
        let toDisplay = ''
        for (let episode of episodes){
            // toDisplay = toDisplay + episode.title
            toDisplay = `${toDisplay}<div>${episode.title}</div>`
        }
        // document.getElementById('result').innerHTML = episodes
        document.getElementById('result').innerHTML = toDisplay
    })
}