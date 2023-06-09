let sendBtnEl = document.getElementById("send-btn")
let chatHistoryEl = document.querySelector(".chat-history")
let userInputEl = document.getElementById("user-input")

let chatBubblesHTML =  `
    <div class="chatbot-bubble"></div>
    <div class="chatbot-bubble"></div>
    <div class="chatbot-bubble"></div>
`

function sendUserQuery (){
    let newElement = document.createElement("div")
    newElement.classList.add("user-message")

    /*Add input only if input is not blank*/
    if (userInputEl.value != ""){
        newElement.textContent = userInputEl.value
        let userMessage = userInputEl.value

        let chatBubbles = document.createElement("div")
        chatBubbles.classList.add("chatbot-typing")
        chatBubbles.innerHTML = chatBubblesHTML


        userInputEl.value = ""
        chatHistoryEl.appendChild(newElement)
        chatHistoryEl.appendChild(chatBubbles)

        /* Trigger transition by accessing the opacity property */
        setTimeout(() => newElement.style.opacity = 1, 10);

    /*Fetch Api*/

    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Process the response from the Flask server
        console.log(data);
        
        let aiResponse = data.response 

        // Create new A.I. Message Div with correct class
        let newAIResponse = document.createElement("div")
        newAIResponse.classList.add("ai-message")

        //Remove chatbubbles
        chatBubbles.remove()

        //Append new message text content and add to chat History
        newAIResponse.innerHTML = aiResponse
        chatHistoryEl.appendChild(newAIResponse)
        
    
        //Sources table
        let resourceTableEl = document.getElementById("resource-table")

        //Table body clear
        let resourceTableBody = document.querySelector("#resource-table tbody")
        resourceTableBody.innerHTML = "";

        let sources = data.sources 

        sources.forEach(item => {
            //Create row
            let row = document.createElement("tr")

            //Cell data for row

            let cell1 = document.createElement("td")
            let cell2 = document.createElement("td")

            cell1.textContent = item[0]
            cell2.innerHTML = `<a href="${item[1]}" target=”_blank” >Link</a>`

            //Add cells to row
            row.appendChild(cell1)
            row.appendChild(cell2)

            //append table
            resourceTableBody.appendChild(row)
        })

        //Resources

        let resources = data.resources 
    
        let resourcePlaceholder = document.getElementById("place-holder-card")

        let resourceCount = 1
        let totalResources = resources.length 

        if (totalResources === 0){

            resourcePlaceholder.textContent = "Sorry no resources were found!"


        }
    

        if (totalResources > 0 && resources){

        resources.forEach(item => {

            resourcePlaceholder.remove()


            const cardsEl = document.querySelector('.cards');

            //Create individual resource
            let resource = document.createElement("div")
            // Add class
            resource.classList.add('cards-item');
            // Set correct attributes
            resource.setAttribute('id', `card-${resourceCount}`);
            

            //Append content of individual resource card
            
                //Images first
                let resourceImg = document.createElement("img");

                resourceImg.setAttribute("src", `${item.image}`);

                resource.appendChild(resourceImg)

                //H3 next
                let resourceHeader = document.createElement("h3");
                resourceHeader.textContent = item.title 
                resource.appendChild(resourceHeader)

                //Description
                let resourcePara = document.createElement("p");
                resourcePara.textContent = item.description
                resource.appendChild(resourcePara)

                //Resource link
                let resourceLink = document.createElement("a")

                resourceLink.setAttribute("href", `${item.link}`)
                resourceLink.setAttribute("target", "_blank")

                resourceLink.textContent = "Click for Resource"

                resource.appendChild(resourceLink)


                // Add the new element to carousel
                cardsEl.appendChild(resource);
                resourceCount += 1

        })}

        resourceCount = 1
        resources.forEach(item =>{

            const carouselNav = document.querySelector('.carousel__nav');

            let navLink = document.createElement("a")

            navLink.setAttribute("href", `#card-${resourceCount}`)

            navLink.setAttribute("class", "slider-nav")

            navLink.textContent = `${resourceCount}`

            carouselNav.appendChild(navLink)

            resourceCount += 1
            
        })

        if (totalResources > 0){

            let foundResources = document.createElement("p")
            foundResources.textContent = `${totalResources} matching resource(s) found!`
            foundResources.setAttribute("class", "foundResources")
            const carouselSection = document.querySelector('.carousel');
            carouselSection.appendChild(foundResources)

        }
        













        //Scroll bottom of Chat
        chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight; 




    })
    .catch(error => {
        console.error('Error:', error);
    });


    }
    
}

sendBtnEl.addEventListener("click", sendUserQuery)


// Get the input field
let inputField = document.getElementById("user-input");

// Execute main function to gather answer and resources when the user presses a key on the keyboard
inputField.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    event.preventDefault();
    // Trigger the button element with a click
    sendBtnEl.click()
  }
});