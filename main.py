from flask import Flask, jsonify, render_template, url_for, request, jsonify, session
import uuid 
from getAssistant import getAssistantResponse


app = Flask(__name__, 
            template_folder="templates", 
            static_folder='static')

#Secret Key that changes to random ID every time user refreshes 
app.secret_key = str(uuid.uuid4())


@app.route('/')
def index():
    #check a brand new session
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]  # Initialize messages if not already present

    #clear messages on refresh 
    elif request.referrer != request.url:
        session['messages'] = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]  

    return render_template("index.html")




@app.route('/chatbot', methods=['POST'])
def chatbot():

    #Get User Input
    user_input = request.json.get('message')

    #Append User Input to Session Messages 
    session['messages'].append({"role": "user", "content": f"{user_input}"})

    # Process the message and generate a response using the OpenAI API
    session_messages = session['messages']

    openAIResponse = getAssistantResponse(user_input, session_messages)

    response = openAIResponse[0]
    session['messages'] = openAIResponse[1]

    session.modified = True
    
    return jsonify(response=response, messages=session['messages'])

if __name__ == '__main__':
     app.jinja_env.auto_reload = True
     app.run(
        debug=True, 
        use_reloader=True, 
            )
