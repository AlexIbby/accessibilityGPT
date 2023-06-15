from flask import Flask, jsonify, render_template, url_for



app = Flask(__name__, 
            template_folder="templates", 
            static_folder='static')



@app.route('/')
def index():
    return render_template("index.html")



if __name__ == '__main__':
     app.jinja_env.auto_reload = True
     app.run(
        debug=True, 
        use_reloader=True, 
            )
