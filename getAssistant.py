import openai
import os 
import re

# Reminder on Structure of Messages from OpenAI Api

# Sytem Level - {"role": "system", "content": "You are a helpful assistant."},
# User Question - {"role": "user", "content": "Who won the world series in 2020?"},
# AI Answer - {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},

openai.api_key = os.getenv("OPENAI_API_KEY")

def getAssistantResponse(session_messages):
    """
    The getAssistantResponse function makes to calls to the OpenAI API. The goal is to first answer the question based on the context. The second then provides the response in HMTL. The reason for doing so is cleaning up the AI response without needing to implement a complex NLP approach to ensure sentences and paragraphs display appropriately. As of July 2023, the OpenAI GPT 3.5 turbo models all need these instructions to be split out. GPT4 is able to follow the instructions and answer and provide the response in HTML, but the cost is high. 
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
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

