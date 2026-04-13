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

KEY_FILE = os.path.join(os.path.dirname(__file__), '.key')

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

app = Flask(__name__, static_folder='.')
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'agent_email.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
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

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/index.html')
def index():
    return send_file('index.html')

@app.route('/Panel.html')
def Panel():
    return send_file('Panel.html')

@app.route('/debug.html')
def Debug():
    return send_file('debug.html')

@app.route('/simple.html')
def Simple():
    return send_file('simple.html')

@app.route('/login.html')
def login():
    return send_file('login.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'ok',
        'database': 'sqlite',
        'version': '1.2'
    })

@app.route('/api/empresas', methods=['GET'])
def get_empresas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, nombre, alias, imap_host, imap_port, email_user, smtp_host, smtp_port, logo_url, activo, created_at
            FROM empresas
            ORDER BY created_at DESC
        ''')
        empresas = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(empresas)
    except Exception as e:
        logger.error(f"Error get_empresas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas', methods=['POST'])
@token_required
def create_empresa():
    data = request.json
    required = ['nombre', 'alias', 'imap_host', 'email_user']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO empresas (nombre, alias, imap_host, imap_port, email_user, email_pass, smtp_host, smtp_port, logo_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nombre'],
            data.get('alias', ''),
            data.get('imap_host', 'imap.gmail.com'),
            data.get('imap_port', 993),
            data['email_user'],
            encrypt_password(data.get('email_pass', '')) if data.get('email_pass') else '',
            data.get('smtp_host', data.get('imap_host', '')),
            data.get('smtp_port', 465),
            data.get('logo_url', '')
        ))
        
        new_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': new_id, 'message': 'Empresa creada correctamente'}), 201
    except Exception as e:
        logger.error(f"Error create_empresa: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/<int:empresa_id>', methods=['PUT'])
@token_required
def update_empresa(empresa_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_fields = []
        params = []
        
        for field in ['nombre', 'alias', 'imap_host', 'imap_port', 'email_user', 'smtp_host', 'smtp_port', 'logo_url']:
            if field in data:
                update_fields.append(f'{field} = ?')
                params.append(data[field])
        
        if 'email_pass' in data and data['email_pass']:
            update_fields.append('email_pass = ?')
            params.append(encrypt_password(data['email_pass']))
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        params.append(empresa_id)
        
        cur.execute(f'''
            UPDATE empresas SET {', '.join(update_fields)}
            WHERE id = ?
        ''', params)
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Empresa no encontrada'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Empresa actualizada correctamente'})
    except Exception as e:
        logger.error(f"Error update_empresa: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/<int:empresa_id>', methods=['DELETE'])
@token_required
def delete_empresa(empresa_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM empresas WHERE id = ?', (empresa_id,))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Empresa no encontrada'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Empresa eliminada correctamente'})
    except Exception as e:
        logger.error(f"Error delete_empresa: {e}")
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/operadores', methods=['GET'])
def get_operadores():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, username, nombre, email, rol, notas, activo, created_at 
            FROM usuarios 
            WHERE activo = 1 
            ORDER BY created_at DESC
        ''')
        operadores = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(operadores)
    except Exception as e:
        logger.error(f"Error get_operadores: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores', methods=['POST'])
@token_required
def create_operador():
    data = request.json
    required = ['username', 'nombre', 'email']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT id FROM usuarios WHERE username = ?', (data['username'],))
        if cur.fetchone():
            conn.close()
            return jsonify({'error': 'El username ya existe'}), 400
        
        password_hash = generate_password_hash(data.get('password', 'temp123'))
        
        cur.execute('''
            INSERT INTO usuarios (username, nombre, email, password_hash, rol, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['username'],
            data['nombre'],
            data['email'],
            password_hash,
            data.get('rol', 'operador'),
            data.get('notas', '')
        ))
        
        new_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': new_id, 'message': 'Operador creado correctamente'}), 201
    except Exception as e:
        logger.error(f"Error create_operador: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores/<username>', methods=['PUT'])
@token_required
def update_operador(username):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_fields = []
        params = []
        
        for field in ['nombre', 'email', 'rol', 'notas']:
            if field in data:
                update_fields.append(f'{field} = ?')
                params.append(data[field])
        
        if 'password' in data and data['password']:
            update_fields.append('password_hash = ?')
            params.append(generate_password_hash(data['password']))
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        params.append(username)
        
        cur.execute(f'''
            UPDATE usuarios SET {', '.join(update_fields)}
            WHERE username = ? AND username != 'admin'
        ''', params)
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Operador no encontrado o no editable'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Operador actualizado correctamente'})
    except Exception as e:
        logger.error(f"Error update_operador: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores/<username>', methods=['DELETE'])
@token_required
def delete_operador(username):
    if username == 'admin':
        return jsonify({'error': 'No se puede eliminar al administrador'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            UPDATE usuarios SET activo = 0 
            WHERE username = ? AND username != 'admin'
        ''', (username,))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Operador no encontrado'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Operador eliminado correctamente'})
    except Exception as e:
        logger.error(f"Error delete_operador: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/imap/test', methods=['POST'])
def test_imap_connection():
    data = request.json
    try:
        with imap_tools.MailBox(data['imap_host']).login(data['email'], data['password']) as mailbox:
            return jsonify({'success': True, 'message': 'Conexión exitosa'})
    except Exception as e:
        logger.error(f"Error test_imap: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/imap/sync/<int:empresa_id>', methods=['POST'])
@token_required
def sync_emails(empresa_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM empresas WHERE id = ?', (empresa_id,))
        empresa = dict(cur.fetchone())
        
        if not empresa or not empresa.get('email_user') or not empresa.get('email_pass'):
            return jsonify({'error': 'Empresa no encontrada o sin credenciales'}), 404
        
        password = decrypt_password(empresa['email_pass'])
        
        with imap_tools.MailBox(empresa['imap_host']).login(empresa['email_user'], password) as mailbox:
            mailbox.folder.set('INBOX')
            messages = list(mailbox.fetch(limit=50))
            
            synced_count = 0
            for msg in reversed(messages):
                archivos = []
                if msg.attachments:
                    for att in msg.attachments:
                        archivos.append({
                            'nombre': att.filename,
                            'tamano': f"{len(att.payload) / 1024:.1f} KB" if att.payload else "0 KB"
                        })
                
                fecha_str = msg.date.strftime('%Y-%m-%dT%H:%M:%S') if msg.date else ''
                thread_id = f"{empresa['email_user']}_{msg.uid}"
                
                cur.execute('SELECT id FROM hilos WHERE thread_id = ?', (thread_id,))
                if not cur.fetchone():
                    para_value = str(msg.to[0]) if isinstance(msg.to, (list, tuple)) and msg.to else empresa['email_user']
                    cur.execute('''
                        INSERT INTO hilos (thread_id, remitente, asunto, mensaje, cuenta_empresa, correo_empresa, fecha, adjuntos, archivos, tamano_total, estado_ticket, leido, de, para)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        thread_id,
                        msg.from_ or '',
                        msg.subject or '',
                        msg.text or msg.html or '',
                        empresa['nombre'],
                        empresa['email_user'],
                        fecha_str,
                        1 if archivos else 0,
                        str(archivos),
                        '0 KB',
                        'PENDIENTE',
                        0,
                        msg.from_ or '',
                        para_value
                    ))
                    synced_count += 1
            
            conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True, 'synced': synced_count})
    except Exception as e:
        logger.error(f"Error sync_emails: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/imap/sync-all', methods=['POST'])
@token_required
def sync_all_emails():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, nombre, alias, imap_host, imap_port, email_user, email_pass FROM empresas WHERE activo = 1 AND email_user IS NOT NULL AND email_pass IS NOT NULL")
        empresas = [dict(row) for row in cur.fetchall()]
        
        results = []
        for empresa in empresas:
            try:
                password = decrypt_password(empresa['email_pass'])
                
                with imap_tools.MailBox(empresa['imap_host']).login(empresa['email_user'], password) as mailbox:
                    mailbox.folder.set('INBOX')
                    messages = list(mailbox.fetch(limit=30))
                    
                    synced_count = 0
                    for msg in reversed(messages):
                        archivos = []
                        if msg.attachments:
                            for att in msg.attachments:
                                archivos.append({
                                    'nombre': att.filename,
                                    'tamano': f"{len(att.payload) / 1024:.1f} KB" if att.payload else "0 KB"
                                })
                        
                        fecha_str = msg.date.strftime('%Y-%m-%dT%H:%M:%S') if msg.date else ''
                        thread_id = f"{empresa['email_user']}_{msg.uid}"
                        
                        cur.execute('SELECT id FROM hilos WHERE thread_id = ?', (thread_id,))
                        if not cur.fetchone():
                            para_value = str(msg.to[0]) if isinstance(msg.to, (list, tuple)) and msg.to else empresa['email_user']
                            cur.execute('''
                                INSERT INTO hilos (thread_id, remitente, asunto, mensaje, cuenta_empresa, correo_empresa, fecha, adjuntos, archivos, tamano_total, estado_ticket, leido, de, para)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                thread_id,
                                msg.from_ or '',
                                msg.subject or '',
                                msg.text or msg.html or '',
                                empresa['nombre'],
                                empresa['email_user'],
                                fecha_str,
                                1 if archivos else 0,
                                str(archivos),
                                '0 KB',
                                'PENDIENTE',
                                0,
                                msg.from_ or '',
                                para_value
                            ))
                            synced_count += 1
                    
                    results.append({'empresa': empresa['nombre'], 'synced': synced_count, 'success': True})
                    
            except Exception as e:
                results.append({'empresa': empresa['nombre'], 'error': str(e), 'success': False})
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"Error sync_all: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hilos', methods=['GET'])
def get_hilos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, thread_id, remitente, asunto, mensaje, cuenta_empresa, correo_empresa,
                   fecha, adjuntos, archivos, tamano_total, estado_ticket, leido, asignado_a, de, para, cc
            FROM hilos
            ORDER BY fecha DESC
            LIMIT 200
        ''')
        hilos = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(hilos)
    except Exception as e:
        logger.error(f"Error get_hilos: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hilos', methods=['POST'])
@token_required
def create_hilo():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO hilos (thread_id, remitente, asunto, mensaje, cuenta_empresa, correo_empresa,
                             fecha, adjuntos, archivos, tamano_total, estado_ticket, leido, 
                             de, para, cc, asignado_a, de_operador)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('thread_id', f'thread_{int(time.time())}'),
            data.get('remitente', ''),
            data.get('asunto', ''),
            data.get('mensaje', ''),
            data.get('cuenta_empresa', ''),
            data.get('correo_empresa', ''),
            data.get('fecha', datetime.now().isoformat()),
            data.get('adjuntos', 0),
            str(data.get('archivos', [])),
            data.get('tamano_total', '0 KB'),
            data.get('estado_ticket', 'PENDIENTE'),
            data.get('leido', 0),
            data.get('de', ''),
            data.get('para', ''),
            data.get('cc', ''),
            data.get('asignado_a', None),
            data.get('de_operador', 0)
        ))
        
        new_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': new_id, 'message': 'Hilo creado correctamente'}), 201
    except Exception as e:
        logger.error(f"Error create_hilo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hilos/<thread_id>', methods=['PUT'])
@token_required
def update_hilo(thread_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_fields = []
        params = []
        
        for field in ['remitente', 'asunto', 'mensaje', 'cuenta_empresa', 'correo_empresa', 'fecha',
                      'adjuntos', 'archivos', 'tamano_total', 'estado_ticket', 'leido', 'asignado_a', 'de', 'para', 'cc']:
            if field in data:
                update_fields.append(f'{field} = ?')
                params.append(data[field])
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        params.append(thread_id)
        
        cur.execute(f'''
            UPDATE hilos SET {', '.join(update_fields)}
            WHERE thread_id = ?
        ''', params)
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Hilo actualizado correctamente'})
    except Exception as e:
        logger.error(f"Error update_hilo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/hilos/<thread_id>', methods=['DELETE'])
@token_required
def delete_hilo(thread_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM hilos WHERE thread_id = ?', (thread_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Hilo eliminado correctamente'})
    except Exception as e:
        logger.error(f"Error delete_hilo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
