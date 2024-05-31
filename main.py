from flask import Flask,render_template, request, jsonify, session
from getAssistant import getAssistantResponse
from getContext import getContext
from flask_session import Session
from resources import matchingResources

app = Flask(__name__,
            template_folder="templates", 
            static_folder='static')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

system_prompt = "You are an assistant created by Alex Ibrahim to provide answers on the Accessibility for Ontarians with Disabilities Act and its regulation the Integrated Accessibility Standards Regulation. Use only the context given to you and the context in this system prompt. If you cannot, simply say 'Sorry, I can't provide an answer based on the context provided to me. Keep responses between 2-6 sentences.  If you provide a link in your answer - use an html anchor element <a></a>. The sources are automatically provided to the user, no need to cite them. If a user asks about a personal circumstance, give an answer but remind them it is general advice that may or may not apply to them. Retrofits for buildings are not required by the AODA. The AODA and its standards also do not cover interior elements of buildings for example washrooms, entrances, elevators and others - these areas are regulated by Ontario's Building Code's barrier free requirements."

@app.route('/')
def index():
    session['messages'] = [
        {"role": "system", "content": system_prompt}
    ]
    return render_template("index.html")


@app.route('/chatbot', methods=['POST'])
def chatbot():

    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": system_prompt}
        ]

        
    # Get User Input
    user_input = request.json.get('message')

    # Get matching resources
    resources = matchingResources(user_input)

    # Get context
    context = getContext(user_input)
    sources = context[1]
    context = context[0]


    # Create a temporary version of session messages with context
    user_input_with_context = session['messages'].copy()

    user_input_with_context.append({"role": "user", "content": f" User Question: {user_input} \n Context Documents: \n\n{context}"})
    

    # Process the message with context and generate a response using the OpenAI API
    openAIResponse = getAssistantResponse(user_input_with_context)

    # Append User Question to Real History without Context
    session['messages'].append({
        "role": "user",
        "content": f"{user_input}"
    })


    # Get Assistant Response
    response = openAIResponse

    # Append AI Response
    session['messages'].append({
        "role": "assistant",
        "content": f"{response}"
    })

    session.modified = True
    session['messages']
    return jsonify(response=response, messages=session['messages'], sources=sources, resources=resources)


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/how-this-works.html')
def how_page():
    return render_template('how.html')

if __name__ == '__main__':
     app.jinja_env.auto_reload = True
     app.run(
        debug=True, 
            )
