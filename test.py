import json, os, random
from flask import Flask, request, render_template, redirect, make_response

app = Flask(__name__)

# classe user che verrà utilizzata per ogni nuovo utente che si registra
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
    
    def getEmail(self):
        return self.Email
    
    def getPassword(self):
        return self.Password

# ogni volta che apro la home verrò loggato come 'Alessio Lodi Rizzini'
@app.route('/', methods=['GET'])
def index():
    devName = 'Alessio Lodi Rizzini'
    return render_template('home.html', dev_name=devName)

# questo invece è un log DINAMICO, ovvero il nome cambierà ogni volta
# @app.route('/<nome>', methods=['GET'])
# def index(nome):
#    return render_template('index.html', dev_name=nome)

# vado a prendere gli utenti dal file json 'users'
@app.route('/users', methods=['GET'])  # accetta solo richieste di tipo GET
def get_users():  # funzione eseguita quando un utente accede all'URL /users
    with open('./users.json', 'r') as file:  # apro il json in modalità di lettura ('r')
        data = json.load(file)  # leggo il contenuto del json e lo trasformo in una lista/dizionario, poi lo immagazzino nella var. data
        userList = []  # lista vuota per gli user 
    
    # Cycle over each JSON object and create a new User object
    for jsonFile in data:  # scorre ogni oggetto nel file json
        user = User(int(jsonFile['ID']), jsonFile['FirstName'], jsonFile['LastName'], jsonFile['Email'], jsonFile['Password'])  # creo lo user 
        userList.append(user)  # metto lo user nella lista precedentemente creata
    
    return render_template('users.html', users=userList)  # passo la lista di utenti al template users.html

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')  # mostra il form di registrazione

# Add user to file
# Path: POST /new
@app.route('/register/create_post', methods=['POST'])  # quando apro la pagina login
def add_user():  # funzione per aggiungere un nuovo user
    # Open user file
    with open('./users.json', 'r') as file:  # apro il file user in modalità lettura
        data = json.load(file)  # leggo il contenuto del json e lo trasformo in una lista/dizionario, poi lo immagazzino nella var. data
    
    # bisogna cercare l'Id dell'ultimo utente per mettere +1 a quello nuovo
    # se non ci sono utenti, viene creato uno nuovo con ID = 1
    lastUserId = data[-1]['ID'] if data else 0  # Verifica se ci sono dati nel file e ottieni l'ID dell'ultimo utente
    lastUserId = lastUserId + 1  # Incrementa l'ID per il nuovo utente
        
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    
    newUser = {
        "ID": lastUserId,
        "FirstName": first_name,
        "LastName": last_name,
        "Email": email,
        "Password": password
    }
    
    data.append(newUser)
    
    with open('./users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    return redirect('/users')

#<<<<<<< HEAD
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

###CREAZIONE ED EVENTUALE CANCELLAZIONE DEI POST

@app.route('/posts', methods=['GET', 'POST'])
def create_posts(): #funzione per creare i post
    user_email = request.cookies.get('user_email') #per ottenere la mail dell'utente loggato tramite i cookie del brawser
    user = None #inizializzo la variabile user come vuota prima di cercare l'utente loggato.

    with open('./users.json', 'r') as file:  #leggo il file json per verificare che l'utente sia loggato
        users = json.load(file) #carico il file letto in users
         
        #per ogni elemento in users, assegna temporaneamente quel singolo elemento alla variabile u
        for u in users: #cicla attraverso tutti gli utenti (u=variabile temporanea che rappresenta ogni elemento della lista users[la lista sarebbe users.json])
            if u['Email'] == user_email: #controllo se l'email corrisponde all'utente loggato
               user = u #salvo l'utente trovato
               break #interrompo il ciclo una volta trovato l'utente
               

    if not user:
       return redirect('/login') #se non c'è nessun utente loggato reindirizza al login
    
    #gestione della richiesta post (aggiungo un nuovo post)
    if request.method == 'POST':
       content = request.form['content'] #leggo il contenuto del post dal modulo inviato
       new_post = {
           "Author": user['Email'], #usa l'email dell'utente come identificatore del post
           "Content": content  #inserisce il contenuto del post
       }

       with open('./posts.json', 'r') as file:
            posts = json.load(file)   #carico i post già esistenti nel file json
        
       posts.append(new_post)
       
       
#=======

### CREAZIONE ED EVENTUALE CANCELLAZIONE DEI POST

@app.route('/posts', methods=['GET', 'POST'])
def create_posts():  # funzione per creare i post
    user_email = request.cookies.get('user_email')  # per ottenere la mail dell'utente loggato tramite i cookie del browser
    user = None  # inizializzo la variabile user come vuota prima di cercare l'utente loggato.

    with open('./users.json', 'r') as file:  # leggo il file json per verificare che l'utente sia loggato
        users = json.load(file)  # carico il file letto in users

        # per ogni elemento in users, assegna temporaneamente quel singolo elemento alla variabile u
        for u in users:  # cicla attraverso tutti gli utenti (u=variabile temporanea che rappresenta ogni elemento della lista users[la lista sarebbe users.json])
            if u['Email'] == user_email:  # controllo se l'email corrisponde all'utente loggato
                user = u  # salvo l'utente trovato
                break  # interrompo il ciclo una volta trovato l'utente

    if not user:
        return redirect('/login')  # se non c'è nessun utente loggato reindirizza al login

    # GESTIONE RICHIESTA POST (aggiungo un nuovo post)
    if request.method == 'POST':
        content = request.form['content']  # leggo il contenuto del post dal modulo inviato
        new_post = {
            "Author": user['Email'],  # usa l'email dell'utente come identificatore del post
            "Content": content  # inserisce il contenuto del post
        }

        with open('./posts.json', 'r') as file:
            posts = json.load(file)  # carico i post già esistenti nel file json

        posts.append(new_post)  # aggiungo un nuovo post alla lista

        with open('./posts.json', 'w') as file:  # salvo la lista aggiornata dei post nel file JSON
            json.dump(posts, file, indent=4)  # Serializza l'oggetto posts (trasforma l'oggetto python in una stringa nel formato json) 

        return redirect('/posts')  # ricarico la pagina per mostrare il post aggiornato

    # GESTIONE DELLA RICHIESTA GET (VISUALIZZO I POST DELL'UTENTE LOGGATO)
    with open('./posts.json', 'r') as file:
        posts = json.load(file)  # carico tutti i post dal file json

    user_posts = [post for post in posts if post['Author'] == user['Email']]  # filtro i post dell'utente loggato

    return render_template('posts.html', posts=user_posts)  # ritorna il template per mostrare i post dell'utente


@app.route('/delete_post/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    user_email = request.cookies.get('user_email')  # ottiengo l'email dell'utente loggato dai cookie del browser
    user = None  # inizializzo la variabile per l'utente come `None`(nulla)

    with open('./users.json', 'r') as file:  # carico gli utenti dal file JSON per verificare se l'utente è loggato
        users = json.load(file)  # leggo il file JSON e lo carico in `users`
        for u in users:  # cicla attraverso gli utenti
            if u['Email'] == user_email:  # controllo se l'email corrisponde all'utente loggato
                user = u  # salvo l'utente trovato
                break  # interrompo il ciclo una volta trovato l'utente

    if not user:  # se non c'è un utente loggato, reindirizzo al login
        return redirect('/login')

    with open('./posts.json', 'r') as file:  # carico i post esistenti dal file JSON
        posts = json.load(file)

    # controllo se l'indice è valido
    if post_index >= 0 and post_index < len(posts):
        # controllo se il post appartiene all'utente loggato
        if posts[post_index]['Author'] == user['Email']:
            # rimuovi il post dall'elenco
            posts.pop(post_index)

            with open('./posts.json', 'w') as file:  # salvo la lista aggiornata dei post nel file JSON
                json.dump(posts, file, indent=4)

    return redirect('/posts')  # ricarica la pagina per mostrare i post aggiornati

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))  # redirigo alla home dopo il logout
    resp.delete_cookie('user_email')  # rimuovo il cookie 'user_email'
    return resp

#avvio del server Flask
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # avvia il server con modalità debug, uso la porta 5001 invece della 5000 perchè la porta 5000 era dedicata ad app.py

