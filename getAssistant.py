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
        model="gpt-3.5-turbo",
        messages= session_messages
    )

    response = response['choices'][0]['message']['content']
    

    return response




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