import os
from datetime import datetime
from config import Config
from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory



app=Flask(__name__)
app.config.from_object(Config)



azure_openai_resource_uri = "https://pr-tech-fair-aoai.openai.azure.com/"
search_endpoint = "https://pr-tech-fair-acs.search.windows.net"

# MAIN ROUTES
@app.route("/", methods=['GET'])
def start():
    print('welcome')
    return render_template('v1/home.html')

@app.route("/about", methods=['GET'])
def about():
    print('about')
    return render_template('v1/about.html')

@app.route("/chat", methods=['GET'])
def chat():
    print('chat')
    return render_template('v1/chat.html')

if __name__=="__main__":
    app.run(debug=True, threaded=True, port=9000)
    #app.run()