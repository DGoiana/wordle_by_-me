from cgitb import html
from random_word import RandomWords
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from pyparsing import Word, one_of
import requests
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def pick_random_word():
    #Instantiate randomizer
    r = RandomWords()
    
    true_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount = 3, minLength=5, maxLength=5)

    while true_word == None or '-' in true_word:
        true_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount = 3, minLength=5, maxLength=5).upper()
    else:
        return true_word

letras = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        session['word'] = pick_random_word()
        session['word'] = session['word'].upper()
        letras.clear()
        print(letras)
        print(session['word'])
        print(len(session['word']))
        letters = []
        letters.append(request.form.get("one"))
        letters.append(request.form.get("two"))
        letters.append(request.form.get("three"))
        letters.append(request.form.get("four"))
        letters.append(request.form.get("five"))
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i] == session['word'][i]:
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html")
        session['a'] = letters
        return redirect(url_for("index2"))

@app.route("/index2", methods=["GET", "POST"])
def index2():
    if request.method == "GET":
        letras.append(session['a'])
        print(letras)
        print(session['word'])
        return render_template("index2.html", word=session['word'], lista=letras)
    else:
        letters = []
        letters.append(request.form.get("one"))
        letters.append(request.form.get("two"))
        letters.append(request.form.get("three"))
        letters.append(request.form.get("four"))
        letters.append(request.form.get("five"))
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i] == session['word'][i]:
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html")
        session['b'] = letters
        return redirect(url_for("index3"))

@app.route("/index3", methods=["GET", "POST"])
def index3():
    if request.method == "GET":
        letras.append(session['b'])
        print(letras)
        print(session['word'])
        return render_template("index3.html", word=session['word'], lista=letras)
    else:
        letters = []
        letters.append(request.form.get("one"))
        letters.append(request.form.get("two"))
        letters.append(request.form.get("three"))
        letters.append(request.form.get("four"))
        letters.append(request.form.get("five"))
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i] == session['word'][i]:
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html")
        session['c'] = letters
        return redirect(url_for("index4"))

@app.route("/index4", methods=["GET", "POST"])
def index4():
    if request.method == "GET":
        letras.append(session['c'])
        print(letras)
        return render_template("index4.html", word=session['word'], lista=letras)
    else:
        letters = []
        letters.append(request.form.get("one"))
        letters.append(request.form.get("two"))
        letters.append(request.form.get("three"))
        letters.append(request.form.get("four"))
        letters.append(request.form.get("five"))
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i] == session['word'][i]:
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html")
        session['d'] = letters
        return redirect(url_for("index5"))

@app.route("/index5", methods=["GET", "POST"])
def index5():
    if request.method == "GET":
        letras.append(session['d'])
        print(letras)
        return render_template("index5.html", word=session['word'], lista=letras)
    else:
        letters = []
        letters.append(request.form.get("one"))
        letters.append(request.form.get("two"))
        letters.append(request.form.get("three"))
        letters.append(request.form.get("four"))
        letters.append(request.form.get("five"))
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i] == session['word'][i]:
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html")
        session['e'] = letters
        return redirect(url_for("index_f"))

@app.route("/index_f", methods=["GET", "POST"])
def index_f():
    if request.method == "GET":
        letras.append(session["e"])
        print(letras)
        return render_template("index_f.html", word=session['word'], lista=letras)