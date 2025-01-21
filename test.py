import json, os, random
from flask import Flask, request, render_template, redirect 

#l'appa Flask utilizza una directory personalizzata per i templates
template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)

#classe user che verrà utilizzata per ogni nuovo utente che si registra
class User:
    def __init__(self, userId, userName, userLastName, userEmail, userPassword):
        self.ID = userId
        self.FirstName = userName
        self.LastName = userLastName
        self.Email = userEmail
        self.Password = userPassword 

    
    def getID(self):
        return self.ID
    
    def getFirstName(self):
        return self.FirstName
    
    def getLastName(self):
        return self.LastName
    
    def getBirthday(self):
        return self.Email
    
    def getNationality(self):
        return self.Password

#ogni volta che apro la home verrò loggato come 'Alessio Lodi Rizzini'
@app.route('/', methods=['GET'])
def index():
    devName = 'Alessio Lodi Rizzini'
    return render_template('home.html', dev_name=devName)

#questo invece è un log DINAMICO, ovvero il nome cambierà ogni volta
#@app.route('/<nome>', methods=['GET'])
#def index(nome):
#    return render_template('index.html', dev_name=nome)


#vado a prender gli utenti dal file json 'users'
@app.route('/users', methods=['GET']) #accetta solo richieste di tipo GET
def get_users(): #funzione eseguita quando un utente accede all'URL /users
    with open('./db/users.json', 'r') as file: #apro il json in modalita di lettura ('r')
        data = json.load(file) #leggo il contenuto del json e lo trasformo in una lista/dizionario, poi lo immagazzino nella var. data
        userList = [] #lista vuota per gli user 
    
    # Cycle over each JSON object and create a new User object
    for jsonFile in data: #scorre ogni oggeto nel file json
        user = User(int(jsonFile['ID']), jsonFile['FirstName'], jsonFile['LastName'], jsonFile['Email'], jsonFile['Password']) #creo lo user 
        userList.append(user) #metto lo user nella lista precedentemente creata
    
    return render_template('users.html', users=userList) #passo la lista di utenti al template users.html

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# Add user to file
# Path: POST /new
@app.route('/register', methods=['POST'])#quando apro la pagina login
def add_user(): #funzione per aggiungere un nuovo user
    # Open user file
    with open('./db/users.json', 'r') as file: #apro il file yser in modalità lettura
        data = json.load(file) #leggo il contenuto del json e lo trasformo in una lista/dizionario, poi lo immagazzino nella var. data
    
    # bisogna cercare l'Id dell'ultimo utente per mettere +1 a quello nuovo
    # se non ci sono utente ne viene creato uno nuvo con ID = 1
    lastUserId = data[-1]['ID']
    if lastUserId != '':
        lastUserId = int(lastUserId) + 1
    else:
        lastUserId = 1
        
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    
    newUser = {
        "ID": lastUserId,
        "FirstName": first_name,
        "LastName": last_name,
        "Email": email,
        "Password": Password
    }
    
    data.append(newUser)
    
    with open('./db/users.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
    
    return redirect('/users')

