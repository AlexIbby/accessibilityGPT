import openai
import os 
import re

# Reminder on Structure of Messages

# Sytem Level - {"role": "system", "content": "You are a helpful assistant."},
# User Question - {"role": "user", "content": "Who won the world series in 2020?"},
# AI Answer - {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},

openai.api_key = os.getenv("OPENAI_API_KEY")

def getAssistantResponse(session_messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages= session_messages
    )

    response = response['choices'][0]['message']['content']    

    response = html_response(response)

    return response

def html_response(text):

    system_prompt = "Your role is take this response and convert it to HTML and remove references to source documents. Put the text inside of paragraph p tags, each paragraph should have a maximum of two setences. If there something in the text that can be a list, put the list inside a <ul> element with the list items in respective <li> elements as needed, no paragraphs needed for li item text. If there are references to context or source documents in the text, you may edit the content remove them as the user already provided the sources and context. If there are web links, put them inside of properly formatted anchor tags <a> and integrate them into the text. Do not edit the content of the text otherwise."

    html_api_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{text}"},
        ]
    ) 

    html_api_response = html_api_response['choices'][0]['message']['content']

    return html_api_response


def add_breaks(text):
    # This pattern captures a sentence ending in ., ?, or !, followed by a space or the end of a string
    # The negative lookbehind assertion (?<!\.\w\w) makes sure we don't split at periods that come after two or more non-space characters
    pattern = r"(?<!\.\w\w)([.!?])\s*"
    
    # This splits the text into a list of sentences
    sentences = re.split(pattern, text)
    
    new_text = ""
    for i in range(0, len(sentences)-1, 3):
        # The -1 is to prevent going over the end of the list, as the last split is usually an empty string
        # The 3 in the step value is to skip over the matched punctuation and whitespace
        sentence = "".join(sentences[i:i+3])
        
        new_text += sentence
        
        # This checks if we're at a multiple of 2 for the sentence count and appends the breaks if so
        if ((i+3)//3) % 2 == 0:
            new_text += " <br><br>"
    
    return new_text.strip()