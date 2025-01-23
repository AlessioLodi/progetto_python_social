import json
import os
from flask import Flask, request, render_template, redirect, make_response

app = Flask(__name__)

# Classe User per ogni nuovo utente che si registra
class User:
    def __init__(self, userId, userName, userLastName, userEmail, userPassword):
        self.ID = userId
        self.FirstName = userName
        self.LastName = userLastName
        self.Email = userEmail
        self.Password = userPassword

    def to_dict(self):
        return {
            "ID": self.ID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Email": self.Email,
            "Password": self.Password
        }

# Pagina principale che manda alla registrazione se non loggato
@app.route('/', methods=['GET'])
def index():
    return redirect('/register')  # Reindirizza direttamente alla pagina di registrazione

# Rotta per la registrazione
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Ottieni i dati dal form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Leggi gli utenti esistenti dal file JSON
        with open('users.json', 'r') as file:
            users = json.load(file)

        # Calcola il prossimo ID
        last_id = users[-1]['ID'] if users else 0
        new_id = last_id + 1

        # Crea il nuovo utente e aggiungilo al file JSON
        new_user = User(new_id, first_name, last_name, email, password)
        users.append(new_user.to_dict())

        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)

        return redirect('/login')

    return render_template('register.html')

# Rotta per il login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Controlla le credenziali nel file JSON
        with open('users.json', 'r') as file:
            users = json.load(file)

        user = next((u for u in users if u['Email'] == email and u['Password'] == password), None)

        if user:
            resp = make_response(redirect('/posts'))
            resp.set_cookie('user_email', email)
            return resp
        else:
            return "Credenziali non valide. Riprova.", 401

    return render_template('login.html')

# Pagina dei post dell'utente loggato
@app.route('/posts', methods=['GET'])
def posts():
    user_email = request.cookies.get('user_email')
    if not user_email:
        return redirect('/login')  # Se non è loggato, reindirizza al login

    # Leggi i post dal file JSON
    with open('posts.json', 'r') as file:
        posts = json.load(file)

    user_posts = [post for post in posts if post['Author'] == user_email]

    return render_template('home.html', posts=user_posts)

# Rotta per creare un nuovo post
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    user_email = request.cookies.get('user_email')
    if not user_email:
        return redirect('/login')  # Se non è loggato, reindirizza al login

    if request.method == 'POST':
        content = request.form['content']

        # Leggi i post esistenti dal file JSON
        with open('posts.json', 'r') as file:
            posts = json.load(file)

        # Aggiungi il nuovo post
        new_post = {
            "Author": user_email,
            "Content": content
        }
        posts.append(new_post)

        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=4)

        return redirect('/posts')

    return render_template('create_post.html')

# Rotta per eliminare un post
@app.route('/delete_post/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    user_email = request.cookies.get('user_email')
    if not user_email:
        return redirect('/login')  # Se non è loggato, reindirizza al login

    # Leggi i post esistenti dal file JSON
    with open('posts.json', 'r') as file:
        posts = json.load(file)

    # Controlla se l'indice è valido e se il post appartiene all'utente loggato
    if 0 <= post_index < len(posts) and posts[post_index]['Author'] == user_email:
        posts.pop(post_index)

        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=4)

    return redirect('/posts')

# Rotta per il logout
@app.route('/logout', methods=['GET'])
def logout():
    user_email = request.cookies.get('user_email')

    # Elimina l'utente dal file JSON
    with open('users.json', 'r') as file:
        users = json.load(file)

    users = [u for u in users if u['Email'] != user_email]

    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

    # Elimina il cookie e reindirizza alla pagina di registrazione
    resp = make_response(redirect('/register'))
    resp.delete_cookie('user_email')
    return resp


# Avvio del server Flask
if __name__ == '__main__':
    # Assicuriamoci che i file JSON esistano
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as file:
            json.dump([], file)

    if not os.path.exists('posts.json'):
        with open('posts.json', 'w') as file:
            json.dump([], file)

    app.run(debug=True, port=5001)
