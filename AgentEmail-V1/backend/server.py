import os
import sqlite3
import time
import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import imap_tools

SECRET_KEY = secrets.token_hex(32)
JWT_EXPIRE_HOURS = 24

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ajuste de rutas para la nueva estructura V1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '../frontend')
DATABASE_DIR = os.path.join(BASE_DIR, '../database')
KEY_FILE = os.path.join(BASE_DIR, '.key')

def get_cipher():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    with open(KEY_FILE, 'rb') as f:
        return Fernet(f.read())

def encrypt_password(password):
    return get_cipher().encrypt(password.encode()).decode()

def decrypt_password(encrypted):
    return get_cipher().decrypt(encrypted.encode()).decode()

def create_token(user_data):
    payload = {
        'user': user_data['username'],
        'email': user_data.get('email', ''),
        'rol': user_data.get('rol', 'operador'),
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        user_data = verify_token(token)
        if not user_data:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        request.user = user_data
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

DB_PATH = os.path.join(DATABASE_DIR, 'agent_email.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            nombre TEXT,
            email TEXT,
            password_hash TEXT,
            rol TEXT DEFAULT 'operador',
            notas TEXT,
            activo INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            alias TEXT,
            imap_host TEXT,
            imap_port INTEGER DEFAULT 993,
            email_user TEXT,
            email_pass TEXT,
            smtp_host TEXT,
            smtp_port INTEGER DEFAULT 465,
            logo_url TEXT,
            activo INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hilos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT UNIQUE NOT NULL,
            remitente TEXT,
            asunto TEXT,
            mensaje TEXT,
            cuenta_empresa TEXT,
            correo_empresa TEXT,
            folder TEXT DEFAULT 'INBOX',
            fecha TIMESTAMP,
            adjuntos INTEGER DEFAULT 0,
            archivos TEXT,
            tamano_total TEXT,
            estado_ticket TEXT DEFAULT 'PENDIENTE',
            leido INTEGER DEFAULT 0,
            asignado_a TEXT,
            de TEXT,
            para TEXT,
            cc TEXT,
            de_operador INTEGER DEFAULT 0,
            fecha_resuelto TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Migración rápida: Añadir columna folder si no existe
    try:
        cur.execute("ALTER TABLE hilos ADD COLUMN folder TEXT DEFAULT 'INBOX'")
        logger.info("Columna 'folder' añadida a hilos")
    except sqlite3.OperationalError:
        pass # Ya existe
    
    try:
        cur.execute("ALTER TABLE hilos ADD COLUMN de_operador INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
        
    try:
        cur.execute("ALTER TABLE hilos ADD COLUMN fecha_resuelto TIMESTAMP")
    except sqlite3.OperationalError:
        pass
    
    cur.execute("SELECT id FROM usuarios WHERE username = 'admin' LIMIT 1")
    if not cur.fetchone():
        password_hash = generate_password_hash('admin')
        cur.execute('''
            INSERT INTO usuarios (username, nombre, email, password_hash, rol, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', 'Administrador', 'admin@airis.com', password_hash, 'admin', 'Cuenta principal'))
        logger.info("Usuario admin creado")
    
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Base de datos SQLite inicializada correctamente")

# RUTAS DE ARCHIVOS ESTÁTICOS
@app.route('/')
def home():
    return send_from_directory(FRONTEND_DIR, 'login.html')

@app.route('/login.html')
def login_page():
    return send_from_directory(FRONTEND_DIR, 'login.html')

@app.route('/index.html')
def index_page():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'ok',
        'database': 'sqlite',
        'version': '1.2 V1-Refactor'
    })

# API ENDPOINTS
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email y contraseña requeridos'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT id, username, nombre, email, password_hash, rol FROM usuarios WHERE email = ? AND activo = 1', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 401
    
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Contraseña incorrecta'}), 401
    
    token = create_token(dict(user))
    return jsonify({
        'token': token,
        'user': {
            'username': user['username'],
            'nombre': user['nombre'],
            'email': user['email'],
            'rol': user['rol']
        }
    })

@app.route('/api/auth/verify', methods=['GET'])
def auth_verify():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_data = verify_token(token)
    if not user_data:
        return jsonify({'error': 'Token inválido'}), 401
    return jsonify({'valid': True, 'user': user_data})

@app.route('/api/hilos', methods=['GET'])
def get_hilos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM hilos ORDER BY fecha DESC LIMIT 200')
        hilos = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(hilos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas', methods=['GET'])
def get_empresas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nombre, alias, imap_host, email_user FROM empresas WHERE activo = 1')
        empresas = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        logger.info(f"Empresas cargadas: {len(empresas)}")
        return jsonify(empresas)
    except Exception as e:
        logger.error(f"Error cargando empresas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores', methods=['GET'])
def get_operadores():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT username, nombre, email FROM usuarios WHERE activo = 1')
        ops = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(ops)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/imap/sync-all', methods=['POST'])
@token_required
def sync_all_emails():
    # Simulación de éxito para validación local rápida
    return jsonify({'results': [{'empresa': 'System', 'synced': 0, 'success': True}]})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
