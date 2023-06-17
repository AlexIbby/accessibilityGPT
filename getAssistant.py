import openai
import os 

# Structure of Messages

# Sytem Level - {"role": "system", "content": "You are a helpful assistant."},
# User Question - {"role": "user", "content": "Who won the world series in 2020?"},
# AI Answer - {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},

openai.api_key = os.getenv("OPENAI_API_KEY")

def getAssistantResponse(user_input, session_messages):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= session_messages
    )

    response = response['choices'][0]['message']['content']

    session_messages.append({
        "role" : "assistant",
        "content": f"{response}"
    })

    return [response, session_messages]





    

