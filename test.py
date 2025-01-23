import json
import os
from flask import Flask, request, render_template, redirect, make_response

# Configurazione Flask
template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
USERS_FILE = './users.json'  # Aggiornato per puntare alla directory principale
POSTS_FILE = './posts.json'

# Funzione per caricare dati JSON
def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return []

# Funzione per salvare dati JSON
def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Crea la directory se non esiste
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

# Funzione per verificare se l'estensione del file è consentita
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotta principale
@app.route('/')
def home():
    posts = load_json(POSTS_FILE)
    user_email = request.cookies.get('user_email')
    users = load_json(USERS_FILE)
    user = next((u for u in users if u['email'] == user_email), None)
    return render_template('home.html', posts=posts, user=user)

# Gestione login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        users = load_json(USERS_FILE)

        # Debug per vedere i dati caricati (opzionale, da rimuovere in produzione)
        print("Dati utenti caricati:", users)

        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            resp = redirect('/')
            resp.set_cookie('user_email', email)
            return resp

        return render_template('login.html', error="Email o password errati. Riprova.")
    return render_template('login.html')

# Registrazione utenti
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        users = load_json(USERS_FILE)

        # Verifica se email o username sono già registrati
        if any(u['email'] == email for u in users):
            return render_template('register.html', error="Email già registrata. Usa un'altra email.")
        if any(u['username'] == username for u in users):
            return render_template('register.html', error="Username già in uso. Scegli un altro username.")

        # Aggiungi nuovo utente
        new_user = {
            "username": username,
            "email": email,
            "password": password
        }
        users.append(new_user)
        save_json(USERS_FILE, users)  # Salva l'utente registrato

        return redirect('/login')
    return render_template('register.html')

# Creazione post
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    user_email = request.cookies.get('user_email')
    user = None

    # Verifica se l'utente è loggato
    if user_email and os.path.exists(USERS_FILE):
        users = load_json(USERS_FILE)
        user = next((u for u in users if u['email'] == user_email), None)

    if not user:
        return redirect('/login')

    if request.method == 'POST':
        content = request.form['content']
        image_url = None

        # Gestione immagine caricata
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                image_path = os.path.join(UPLOAD_FOLDER, image.filename)
                image.save(image_path)
                image_url = f'/static/images/{image.filename}'

        posts = load_json(POSTS_FILE)
        posts.append({'author': user['username'], 'content': content, 'image_url': image_url})
        save_json(POSTS_FILE, posts)

        return redirect('/')

    return render_template('create_post.html')

# Logout
@app.route('/logout')
def logout():
    resp = redirect('/')
    resp.delete_cookie('user_email')
    return resp

# Avvio dell'app
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
