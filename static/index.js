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
        newAIResponse.textContent = aiResponse
        chatHistoryEl.appendChild(newAIResponse)

        //Scroll bottom
        chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight; 

    })
    .catch(error => {
        console.error('Error:', error);
    });

    


    }
    
    

    
}

sendBtnEl.addEventListener("click", sendUserQuery)


