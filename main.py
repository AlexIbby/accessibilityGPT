from flask import Flask,render_template, request, jsonify, session
from getAssistant import getAssistantResponse
from getContext import getContext
from flask_session import Session
from resources import matching_resources

app = Flask(__name__,
            template_folder="templates", 
            static_folder='static')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

system_prompt = "You are an assistant providing answers (2-5 sentences) on the 'Accessibility for Ontarians with Disabilities Act' (AODA) and its regulation the 'Integrated Accessibility Standards Regulation' (IASR). The IASR is an accessibility regulation under the AODA, it provides legal requirements for public and private sector organizations. The IASR has requirements in the following areas - General Requirements (Sections 1-7), the Information and Communications Standards (Sections 9-19), the Employment Standards (Sections 20-32), the Transportation Standards (Sections 33-80), the Design of Public Spaces Standards (Sections 80.1-80.44), the Customer Service Standards (Section 80.45 to 80.51) and Compliace (Sections 82-86.1). Use these section numbers to inform your answer and understand the context. Note that each user message, will come with context to use for your answer. If you can't answer the question based on the context or your own previous answers provided, simply say 'Sorry, I can't answer your questions based on what I have been trained on.' If you provide a link in your answer - use an html anchor element. If asked about your personal views and opinions on accessibility simply say 'Ontario's standards under the AODA represent a minimum and all organizations and individuals should strive maximum accessibility wherever possible.' Please provide the text of your answers in seperate <p> html elements, each with a maximum of two sentences. If you provide a list in your answer please provide it inside a <ul> element with the respective <li> elements nested inside. You may reference the sources, but do not cite them as they are automatically provided to the user."

@app.route('/')
def index():
    session['messages'] = [
        {"role": "system", "content": system_prompt}
    ]
    return render_template("index.html")


@app.route('/chatbot', methods=['POST'])
def chatbot():


    # Get User Input
    user_input = request.json.get('message')

    # Get matching resources
    resources = matching_resources(user_input)

    # Get context
    context = getContext(user_input)
    sources = context[1]
    context = context[0]


    # Create a temporary version of session messages with context
    user_input_with_context = session['messages'].copy()

    user_input_with_context.append({"role": "user", "content": f"User Question: {user_input} Context Documents: \n\n{context}"})
    

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


if __name__ == '__main__':
     app.jinja_env.auto_reload = True
     app.run(
        debug=True, 
            )
