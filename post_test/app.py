from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index() :
    return render_template('index.html')

@app.route('/signUp', methods=['POST'])
def signUp() :
    email = request.form.get('email')
    password = request.form.get('password')
    
    adminEmail = "qwer@qwer.com"
    adminPassword = "1234512345"
    
    msg = ""
    
    if email==adminEmail and password==adminPassword :
        msg = "Hello, administrator"
    elif email==adminEmail and password!=adminPassword :
        msg = "Wrong password, please check again"
    else :
        msg = "f**k you"
    
    return render_template('signUp.html', sentence=msg)