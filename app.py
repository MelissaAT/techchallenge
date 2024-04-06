import os
from datetime import datetime
from config import Config
from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory, jsonify
from azure import generate_openai_completion


app=Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['APP_SECRET']

# MAIN ROUTES
@app.route("/", methods=['GET'])
def start():
    print('welcome')
    if 'response' in session:
        session.pop('response')
    return render_template('v1/home.html')

@app.route("/about", methods=['GET'])
def about():
    print('about')
    return render_template('v1/about.html')

@app.route("/chat_i", methods=['GET'])
def chat_home():
    print('chat')
    if 'response' in session:
        response = session.get('response')
        return render_template('v1/chat.html', response = response["completion_response"])
    return render_template('v1/chat.html')
@app.route("/chat", methods=['POST'])
async def handle_completion():
    user_query = request.form.get("user-query")
    if user_query:
        response = await generate_openai_completion(user_query)
        session["response"] = response
        return redirect(url_for('chat_home'))
    else:
        return jsonify({"error": "Missing user query"}), 400

if __name__=="__main__":
    app.run(debug=True, threaded=True, port=9000)
    #app.run()