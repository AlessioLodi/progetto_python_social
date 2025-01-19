from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Impostare la chiave segreta per le sessioni
app.secret_key = 'una-chiave-segreta'

# Cartella per il salvataggio delle immagini
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# File JSON
USERS_FILE = 'users.json'
POSTS_FILE = 'posts.json'


def allowed_file(filename):
    """Controlla se il file è un'immagine supportata."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_data(filename):
    """Carica i dati da un file JSON."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(filename, data):
    """Salva i dati in un file JSON."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/')
def home():
    posts = load_data(POSTS_FILE)
    user = None

    if 'user_email' in session:
        users = load_data(USERS_FILE)
        for u in users:
            if u['email'] == session['user_email']:
                user = u
                break
    
    return render_template('home.html', posts=posts, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_data(USERS_FILE)
        for user in users:
            if user['email'] == email and check_password_hash(user['password'], password):
                session['user_email'] = email
                return redirect(url_for('home'))

        error_message = "Email o password errati. Riprova."
        return render_template('login.html', error=error_message)
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = load_data(USERS_FILE)

        for user in users:
            if user['email'] == email:
                return "Email già registrata. Usa un'altra email."

        new_user = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password)
        }
        users.append(new_user)
        save_data(USERS_FILE, users)

        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_email' not in session:
        return redirect(url_for('login'))  # Se l'utente non è loggato, lo redirigi alla pagina di login

    if request.method == 'POST':
        author = request.form['author']
        content = request.form['content']

        # Gestione dell'immagine
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f'/static/images/{filename}'

        # Aggiungi il nuovo post
        posts = load_data(POSTS_FILE)
        new_post = {
            'author': author,
            'content': content,
            'image_url': image_url
        }
        posts.append(new_post)
        save_data(POSTS_FILE, posts)

        return redirect(url_for('home'))

    return render_template('create_post.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

