import requests
import json
from random_word import RandomWords
import random
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
import enchant

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

def listToString(s: list): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1.lower()

def api(word: str, lan: str, idd: str, key: str):
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + lan + "/" + word.lower()
    r = requests.get(url = url, headers={"app_id": idd, "app_key": key}).json()
    try:
        return r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    except KeyError:
        return "No definition found"

def pick_random_word():
    #Instantiate randomizer
    r = RandomWords()
    
    true_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount = 3, minLength=5, maxLength=5)

    while true_word == None or '-' in true_word:
        true_word = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb,adjective", minDictionaryCount = 3, minLength=5, maxLength=5)
    else:
        return true_word

def principal(word: str, guess: list):

    def find(word: str, char: str):
        positions = []
        pos = word.find(char)
        while pos != -1:
            positions.append(pos)
            pos = word.find(char, pos + 1)

        return positions
    
    def compare(word: str, guess: list):
        output = ['_'] * len(word)
        counted_pos = set()

        for i in range(len(word)):
            if guess[i] == word[i]:
                output[i] = '*'
                counted_pos.add(i)

        for i in range(len(guess)):
            if guess[i] in word and output[i] != '*':
                positions = find(word, guess[i])
                for pos in positions:
                    if pos not in counted_pos:
                        output[i] = '-'
                        counted_pos.add(pos)
                        break
        
        return output

    final = compare(word, guess)
    return final

def help(encrypt: list):
    possible = [0,1,2,3,4]
    for i in range(len(encrypt)):
        if encrypt[i] == '*':
            possible.remove(i)
    print(possible)
    return random.choice(possible)

d = enchant.Dict('en_US')


letras = []
encrypt = []
check = ['']
check2 = ['']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        session['app_id'] = "9874e239"
        session['app_key'] = "999cef01623851025e0a18b19ea8ae28"
        session['language'] = "en-gb"
        session['ajuda'] = 1
        return render_template("index.html", help=session['ajuda'])
    else:
        if check[0] == '':
            session['word'] = pick_random_word()
            session['word'] = session['word'].upper()
        session['explanation'] = api(session['word'], session['language'], session['app_id'], session['app_key'])
        if d.check(session['word']) == False:
            flash("Our bad!")
            return redirect(url_for('index'))
        for i in range(len(session['word'])):
            if ord(session['word'][i]) < 65 or ord(session['word'][i]) > 90:
                flash("Our bad!")
                return redirect(url_for('index'))
        letras.clear()
        encrypt.clear()
        print(letras)
        print(session['word'])
        #print(len(session['word']))
        letters = []
        letters.append(request.form.get("one").upper())
        letters.append(request.form.get("two").upper())
        letters.append(request.form.get("three").upper())
        letters.append(request.form.get("four").upper())
        letters.append(request.form.get("five").upper())
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i].lower() == session['word'][i].lower():
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html", word=session['word'], explanation=session['explanation'])
        if d.check(listToString(letters)) == False:
            flash('Invalid Word!')
            check[0] = '.'
            print(check[0])
            return redirect(url_for('index'))
        session['a'] = letters
        return redirect(url_for("index2"))


@app.route("/index2", methods=["GET", "POST"])
def index2():
    if request.method == "GET":
        check[0] = ''
        print(check2[0])
        if check2[0] == '':
            letras.append(session['a'])
            encrypt.append(principal(session['word'], letras[0]))
        print(letras)
        print(encrypt)
        pos = help(encrypt[0])
        print(pos)
        ajuda = session['word'][pos]
        #print(session['word'])
        session['ajuda'] = 4
        return render_template("index2.html", crypt=encrypt, lista=letras, pos=pos + 1, ajuda=ajuda, help=session['ajuda'])
    else:
        check2[0] = ''
        letters = []
        letters.append(request.form.get("one").upper())
        letters.append(request.form.get("two").upper())
        letters.append(request.form.get("three").upper())
        letters.append(request.form.get("four").upper())
        letters.append(request.form.get("five").upper())
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i].lower() == session['word'][i].lower():
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html", word=session['word'], explanation=session['explanation'])
        if d.check(listToString(letters)) == False:
            flash('Invalid Word!')
            check2[0] = '.'
            return redirect(url_for('index2'))
        session['b'] = letters
        return redirect(url_for("index3"))

@app.route("/index3", methods=["GET", "POST"])
def index3():
    if request.method == "GET":
        print(check2[0])
        if check2[0] == '':
            letras.append(session['b'])
            encrypt.append(principal(session['word'], letras[1]))
        print(encrypt)
        pos = help(encrypt[1])
        print(pos)
        ajuda = session['word'][pos]
        print(letras)
        print(session['word'])  
        return render_template("index3.html", crypt=encrypt, lista=letras, pos=pos + 1, ajuda=ajuda, help=session['ajuda'])
    else:
        check2[0] = ''
        letters = []
        letters.append(request.form.get("one").upper())
        letters.append(request.form.get("two").upper())
        letters.append(request.form.get("three").upper())
        letters.append(request.form.get("four").upper())
        letters.append(request.form.get("five").upper())
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i].lower() == session['word'][i].lower():
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html", word=session['word'], explanation=session['explanation'])
        if d.check(listToString(letters)) == False:
            flash('Invalid Word!')
            check2[0] = '.'
            return redirect(url_for('index3'))
        session['c'] = letters
        return redirect(url_for("index4"))

@app.route("/index4", methods=["GET", "POST"])
def index4():
    if request.method == "GET":
        print(check2[0])
        if check2[0] == '':
            letras.append(session['c'])
            encrypt.append(principal(session['word'], letras[2]))
        pos = help(encrypt[2])
        print(pos)
        ajuda = session['word'][pos]
        print(letras)
        return render_template("index4.html", crypt=encrypt, lista=letras, pos=pos + 1, ajuda=ajuda, help=session['ajuda'])
    else:
        check2[0] = ''
        letters = []
        letters.append(request.form.get("one").upper())
        letters.append(request.form.get("two").upper())
        letters.append(request.form.get("three").upper())
        letters.append(request.form.get("four").upper())
        letters.append(request.form.get("five").upper())
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i].lower() == session['word'][i].lower():
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html", word=session['word'], explanation=session['explanation'])
        if d.check(listToString(letters)) == False:
            check2[0] = '.'
            flash('Invalid Word!')
            return redirect(url_for('index4'))
        session['d'] = letters
        return redirect(url_for("index5"))

@app.route("/index5", methods=["GET", "POST"])
def index5():
    if request.method == "GET":
        print(check2[0])
        if check2[0] == '':
            letras.append(session['d'])
            encrypt.append(principal(session['word'], letras[3]))
        pos = help(encrypt[3])
        print(pos)
        ajuda = session['word'][pos]
        print(letras)
        print(encrypt)
        return render_template("index5.html", crypt=encrypt, lista=letras, pos=pos + 1, ajuda=ajuda, help=session['ajuda'])
    else:
        check2[0] = ''
        letters = []
        letters.append(request.form.get("one").upper())
        letters.append(request.form.get("two").upper())
        letters.append(request.form.get("three").upper())
        letters.append(request.form.get("four").upper())
        letters.append(request.form.get("five").upper())
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i].lower() == session['word'][i].lower():
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html", word=session['word'], explanation=session['explanation'])
        if d.check(listToString(letters)) == False:
            flash('Invalid Word!')
            check2[0] = '.'
            return redirect(url_for('index5'))
        session['e'] = letters
        return redirect(url_for("index6"))

@app.route("/index6", methods=["GET", "POST"])
def index6():
    if request.method == "GET":
        if request.method == "GET":
            print(check2[0])
        if check2[0] == '':
            letras.append(session['e'])
            encrypt.append(principal(session['word'], letras[4]))
        pos = help(encrypt[4])
        print(pos)
        ajuda = session['word'][pos]
        print(letras)
        print(encrypt)
        return render_template("index6.html", crypt=encrypt, lista=letras, pos=pos + 1, ajuda=ajuda, help=session['ajuda'])
    else:
        check2[0] = ''
        letters = []
        letters.append(request.form.get("one").upper())
        letters.append(request.form.get("two").upper())
        letters.append(request.form.get("three").upper())
        letters.append(request.form.get("four").upper())
        letters.append(request.form.get("five").upper())
        count = 0
        for i in range(0, len(session['word'])):
            if letters[i].lower() == session['word'][i].lower():
                count = count + 1
        if count == len(session['word']):
            return render_template("gg.html", word=session['word'], explanation=session['explanation'])
        if d.check(listToString(letters)) == False:
            flash('Invalid Word!')
            check2[0] = '.'
            return redirect(url_for('index6'))
        session['f'] = letters
        return redirect(url_for("index_f"))
    
@app.route("/index_f", methods=["GET", "POST"])
def index_f():
    if request.method == "GET":
        print(check2[0])
        session['ajuda'] = 2
        if check2[0] == '':
            letras.append(session["f"])
            encrypt.append(principal(session['word'], letras[5]))
        print(letras)
        print(encrypt)
        #print(letras)
        return render_template("index_f.html", crypt=encrypt, lista=letras, word=session['word'], help=session['ajuda'], explanation=session['explanation'])
    
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        print(check2[0])
        check2[0] = ''
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
