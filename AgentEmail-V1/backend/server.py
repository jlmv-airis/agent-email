import os
import sqlite3
import time
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from cryptography.fernet import Fernet
import imap_tools
import sys
from pathlib import Path

# Agregar backend al path para importar config y logger
sys.path.insert(0, str(Path(__file__).parent))

# Importar configuración centralizada
from config import config
from logger_config import logger
from security import security, validator
from health import HealthChecker
from database import db_manager
from backup_manager import backup_manager
from init_db import init_database, backup_before_migration

# Log de configuración cargada
logger.info(f"🔧 Configuración cargada: ENVIRONMENT={config.ENVIRONMENT}, DEBUG={config.DEBUG}")

# Rutas usando config
BASE_DIR = config.BASE_DIR
FRONTEND_DIR = config.FRONTEND_DIR
DATABASE_DIR = config.DATABASE_DIR
KEY_FILE = config.ENCRYPTION_KEY_FILE
SECRET_KEY = config.SECRET_KEY
JWT_EXPIRE_HOURS = config.JWT_EXPIRE_HOURS

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

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user.get('rol') != 'admin':
            return jsonify({'error': 'Acceso solo para administradores'}), 403
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__, static_folder=FRONTEND_DIR)

# Configurar CORS con whitelist
CORS(app, resources={
    r"/api/*": {
        "origins": config.CORS_ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-API-Key"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Inicializar módulo de seguridad
security.init_app(app)
logger.info("✅ Security headers y CORS configurados")

DB_PATH = os.path.join(DATABASE_DIR, 'agent_email.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializar base de datos con nueva arquitectura"""
    init_database()  # Importado de init_db.py
    logger.info("✅ Base de datos SQLite inicializada correctamente")

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

@app.route('/api/health')
def health():
    """Health check endpoint para monitoreo"""
    status_data, http_code = HealthChecker.get_health_status()
    return jsonify(status_data), http_code

# API ENDPOINTS
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.json
    
    # Validar estructura JSON
    valid, msg = validator.validate_json_request(
        data,
        required_fields=['email', 'password'],
        field_types={'email': str, 'password': str}
    )
    if not valid:
        logger.warning(f"Login attempt with invalid data: {msg}")
        return jsonify({'error': f"Datos inválidos: {msg}"}), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    # Validar email
    valid, msg = validator.validate_email(email)
    if not valid:
        logger.warning(f"Login attempt with invalid email: {email}")
        return jsonify({'error': f"Email inválido: {msg}"}), 400
    
    if not password:
        return jsonify({'error': 'Contraseña requerida'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT id, username, nombre, email, password_hash, rol FROM usuarios WHERE email = ? AND activo = 1', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if not user:
        logger.warning(f"Login failed: user not found ({email})")
        return jsonify({'error': 'Usuario no encontrado'}), 401
    
    if not check_password_hash(user['password_hash'], password):
        logger.warning(f"Login failed: invalid password ({email})")
        return jsonify({'error': 'Contraseña incorrecta'}), 401
    
    logger.info(f"✅ Login exitoso: {email}")
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

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Total hoy (24h)
        hace_24h = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("SELECT COUNT(*) FROM hilos WHERE fecha >= ?", (hace_24h,))
        total_hoy = cur.fetchone()[0]
        
        # Pendientes
        cur.execute("SELECT COUNT(*) FROM hilos WHERE estado_ticket = 'PENDIENTE'")
        pendientes = cur.fetchone()[0]
        
        # Resueltos (hoy)
        hoy_str = datetime.now().strftime('%Y-%m-%d')
        cur.execute("SELECT COUNT(*) FROM hilos WHERE estado_ticket = 'CERRADO' AND (fecha_resuelto LIKE ? OR created_at LIKE ?)", (hoy_str+'%', hoy_str+'%'))
        resueltos = cur.fetchone()[0]
        
        # Asignados
        cur.execute("SELECT COUNT(*) FROM hilos WHERE estado_ticket = 'ASIGNADO'")
        asignados = cur.fetchone()[0]
        
        # Respondidos
        cur.execute("SELECT COUNT(*) FROM hilos WHERE estado_ticket = 'RESPONDIDO'")
        respondidos = cur.fetchone()[0]

        cur.close()
        conn.close()
        
        return jsonify({
            'total_hoy': total_hoy,
            'pendientes': pendientes,
            'resueltos_hoy': resueltos,
            'asignados': asignados,
            'respondidos': respondidos
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/hilos/update', methods=['PUT'])
@token_required
def update_hilo():
    try:
        data = request.json
        tid = data.get('thread_id')
        estado = data.get('estado')
        asignado_a = data.get('asignado_a')
        leido = data.get('leido') # Nuevo campo
        
        if not tid:
            return jsonify({'error': 'thread_id requerido'}), 400
            
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Obtener información actual del hilo para sincronización IMAP
        cur.execute("SELECT * FROM hilos WHERE thread_id = ?", (tid,))
        hilo_actual = cur.fetchone()
        if not hilo_actual:
            cur.close()
            conn.close()
            return jsonify({'error': 'Hilo no encontrado'}), 404

        updates = []
        params = []
        
        if estado:
            updates.append("estado_ticket = ?")
            params.append(estado)
            if estado == 'CERRADO':
                updates.append("fecha_resuelto = ?")
                params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        if asignado_a is not None:
            if asignado_a != "":
                cur.execute(
                    "SELECT id FROM usuarios WHERE username = ? AND activo = 1 LIMIT 1",
                    (asignado_a,)
                )
                if not cur.fetchone():
                    return jsonify({'error': 'Operador no valido o inactivo'}), 400
            updates.append("asignado_a = ?")
            params.append(asignado_a)
            if asignado_a != "":
                updates.append("estado_ticket = 'ASIGNADO'")

        if leido is not None:
            updates.append("leido = ?")
            params.append(1 if leido else 0)
        
        if not updates:
            cur.close()
            conn.close()
            return jsonify({'error': 'Nada que actualizar'}), 400
            
        params.append(tid)
        query = f"UPDATE hilos SET {', '.join(updates)} WHERE thread_id = ?"
        cur.execute(query, params)
        conn.commit()

        # --- SINCRONIZACIÓN IMAP (Solo si cambió el estado de lectura) ---
        if leido is not None:
            try:
                # Obtener credenciales de la empresa
                cur.execute("SELECT * FROM empresas WHERE nombre = ? LIMIT 1", (hilo_actual['cuenta_empresa'],))
                emp = cur.fetchone()
                if emp:
                    password = decrypt_password(emp['email_pass'])
                    # Extraer UID del thread_id (formato: email_UID)
                    raw_uid = tid.replace(f"{emp['email_user']}_", "")
                    
                    with imap_tools.MailBox(emp['imap_host'], port=emp['imap_port']).login(emp['email_user'], password, initial_folder=hilo_actual['folder'] or 'INBOX') as mailbox:
                        mailbox.flag(raw_uid, imap_tools.MailMessageFlags.SEEN, leido)
                        logger.info(f"Sincronizado IMAP: {tid} leido={leido}")
            except Exception as imap_err:
                logger.error(f"Error sincronizando IMAP para {tid}: {imap_err}")
                # No bloqueamos la respuesta principal si falla IMAP, pero lo logueamos

        cur.close()
        conn.close()
        
        return jsonify({'status': 'ok', 'message': 'Ticket actualizado y sincronizado'})
    except Exception as e:
        logger.error(f"Error en update_hilo: {e}")
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
@token_required
def get_operadores():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, nombre, email, rol FROM usuarios WHERE activo = 1 AND rol IN ('admin', 'operador') ORDER BY username")
        ops = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(ops)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/colaboradores', methods=['GET'])
@admin_required
def get_colaboradores():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, nombre, email, rol, activo, created_at
            FROM usuarios
            WHERE rol IN ('admin', 'operador')
            ORDER BY created_at DESC
        """)
        colaboradores = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(colaboradores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/colaboradores', methods=['POST'])
@admin_required
def create_colaborador():
    try:
        data = request.json or {}
        username = (data.get('username') or '').strip().lower()
        nombre = (data.get('nombre') or '').strip()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        rol = (data.get('rol') or 'operador').strip().lower()

        if not username or not email or not password:
            return jsonify({'error': 'username, email y password son obligatorios'}), 400
        if rol not in ('operador', 'admin'):
            return jsonify({'error': 'rol invalido'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM usuarios WHERE username = ? LIMIT 1", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'El username ya existe'}), 400
        cur.execute("SELECT id FROM usuarios WHERE email = ? LIMIT 1", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'El email ya esta registrado'}), 400

        password_hash = generate_password_hash(password)
        cur.execute("""
            INSERT INTO usuarios (username, nombre, email, password_hash, rol, notas, activo)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (username, nombre or username, email, password_hash, rol, 'Creado desde panel admin'))
        new_id = cur.lastrowid
        conn.commit()

        cur.execute("SELECT id, username, nombre, email, rol, activo, created_at FROM usuarios WHERE id = ?", (new_id,))
        created = dict(cur.fetchone())
        cur.close()
        conn.close()
        return jsonify({'status': 'ok', 'colaborador': created}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/colaboradores/<int:user_id>', methods=['PUT'])
@admin_required
def update_colaborador(user_id):
    try:
        data = request.json or {}
        nombre = (data.get('nombre') or '').strip()
        email = (data.get('email') or '').strip().lower()
        rol = (data.get('rol') or 'operador').strip().lower()
        activo = 1 if data.get('activo', True) else 0
        password = data.get('password') or ''

        if rol not in ('operador', 'admin'):
            return jsonify({'error': 'rol invalido'}), 400
        if not email:
            return jsonify({'error': 'email es obligatorio'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM usuarios WHERE id = ? LIMIT 1", (user_id,))
        existing = cur.fetchone()
        if not existing:
            cur.close()
            conn.close()
            return jsonify({'error': 'Colaborador no encontrado'}), 404

        cur.execute("SELECT id FROM usuarios WHERE email = ? AND id != ? LIMIT 1", (email, user_id))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'El email ya esta registrado'}), 400

        if password:
            password_hash = generate_password_hash(password)
            cur.execute("""
                UPDATE usuarios
                SET nombre = ?, email = ?, rol = ?, activo = ?, password_hash = ?
                WHERE id = ?
            """, (nombre or existing['username'], email, rol, activo, password_hash, user_id))
        else:
            cur.execute("""
                UPDATE usuarios
                SET nombre = ?, email = ?, rol = ?, activo = ?
                WHERE id = ?
            """, (nombre or existing['username'], email, rol, activo, user_id))

        conn.commit()
        cur.execute("SELECT id, username, nombre, email, rol, activo, created_at FROM usuarios WHERE id = ?", (user_id,))
        updated = dict(cur.fetchone())
        cur.close()
        conn.close()
        return jsonify({'status': 'ok', 'colaborador': updated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/colaboradores/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_colaborador(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM usuarios WHERE id = ? LIMIT 1", (user_id,))
        existing = cur.fetchone()
        if not existing:
            cur.close()
            conn.close()
            return jsonify({'error': 'Colaborador no encontrado'}), 404
        if existing['username'] == 'admin':
            cur.close()
            conn.close()
            return jsonify({'error': 'No se puede desactivar la cuenta admin principal'}), 400

        cur.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/empresas', methods=['GET'])
@admin_required
def get_empresas_admin():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, alias, imap_host, imap_port, email_user, smtp_host, smtp_port, activo, created_at
            FROM empresas
            ORDER BY created_at DESC
        """)
        empresas_admin = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(empresas_admin)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/empresas', methods=['POST'])
@admin_required
def create_empresa_admin():
    try:
        data = request.json or {}
        nombre = (data.get('nombre') or '').strip()
        alias = (data.get('alias') or '').strip()
        imap_host = (data.get('imap_host') or '').strip()
        imap_port = int(data.get('imap_port') or 993)
        email_user = (data.get('email_user') or '').strip().lower()
        email_pass = data.get('email_pass') or ''
        smtp_host = (data.get('smtp_host') or '').strip()
        smtp_port = int(data.get('smtp_port') or 465)

        if not nombre or not imap_host or not email_user or not email_pass:
            return jsonify({'error': 'nombre, imap_host, email_user y email_pass son obligatorios'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM empresas WHERE email_user = ? LIMIT 1", (email_user,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'La cuenta de correo ya existe'}), 400

        encrypted_pass = encrypt_password(email_pass)
        cur.execute("""
            INSERT INTO empresas (nombre, alias, imap_host, imap_port, email_user, email_pass, smtp_host, smtp_port, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (nombre, alias, imap_host, imap_port, email_user, encrypted_pass, smtp_host, smtp_port))
        new_id = cur.lastrowid
        conn.commit()
        cur.execute("""
            SELECT id, nombre, alias, imap_host, imap_port, email_user, smtp_host, smtp_port, activo, created_at
            FROM empresas WHERE id = ?
        """, (new_id,))
        created = dict(cur.fetchone())
        cur.close()
        conn.close()
        return jsonify({'status': 'ok', 'empresa': created}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/empresas/<int:empresa_id>', methods=['PUT'])
@admin_required
def update_empresa_admin(empresa_id):
    try:
        data = request.json or {}
        nombre = (data.get('nombre') or '').strip()
        alias = (data.get('alias') or '').strip()
        imap_host = (data.get('imap_host') or '').strip()
        imap_port = int(data.get('imap_port') or 993)
        email_user = (data.get('email_user') or '').strip().lower()
        email_pass = data.get('email_pass') or ''
        smtp_host = (data.get('smtp_host') or '').strip()
        smtp_port = int(data.get('smtp_port') or 465)
        activo = 1 if data.get('activo', True) else 0

        if not nombre or not imap_host or not email_user:
            return jsonify({'error': 'nombre, imap_host y email_user son obligatorios'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM empresas WHERE id = ? LIMIT 1", (empresa_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'Empresa no encontrada'}), 404

        cur.execute("SELECT id FROM empresas WHERE email_user = ? AND id != ? LIMIT 1", (email_user, empresa_id))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'La cuenta de correo ya existe'}), 400

        if email_pass:
            encrypted_pass = encrypt_password(email_pass)
            cur.execute("""
                UPDATE empresas
                SET nombre = ?, alias = ?, imap_host = ?, imap_port = ?, email_user = ?, email_pass = ?, smtp_host = ?, smtp_port = ?, activo = ?
                WHERE id = ?
            """, (nombre, alias, imap_host, imap_port, email_user, encrypted_pass, smtp_host, smtp_port, activo, empresa_id))
        else:
            cur.execute("""
                UPDATE empresas
                SET nombre = ?, alias = ?, imap_host = ?, imap_port = ?, email_user = ?, smtp_host = ?, smtp_port = ?, activo = ?
                WHERE id = ?
            """, (nombre, alias, imap_host, imap_port, email_user, smtp_host, smtp_port, activo, empresa_id))

        conn.commit()
        cur.execute("""
            SELECT id, nombre, alias, imap_host, imap_port, email_user, smtp_host, smtp_port, activo, created_at
            FROM empresas WHERE id = ?
        """, (empresa_id,))
        updated = dict(cur.fetchone())
        cur.close()
        conn.close()
        return jsonify({'status': 'ok', 'empresa': updated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/empresas/<int:empresa_id>', methods=['DELETE'])
@admin_required
def delete_empresa_admin(empresa_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM empresas WHERE id = ? LIMIT 1", (empresa_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'Empresa no encontrada'}), 404
        cur.execute("UPDATE empresas SET activo = 0 WHERE id = ?", (empresa_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/db-stats', methods=['GET'])
@admin_required
def get_db_stats():
    """Obtener estadísticas de la base de datos"""
    try:
        stats = db_manager.get_database_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/db-optimize', methods=['POST'])
@admin_required
def optimize_database():
    """Ejecutar optimizaciónes de BD (ANALYZE, VACUUM)"""
    try:
        logger.info("🔧 Iniciando optimización de BD...")
        stats = db_manager.optimize_all()
        return jsonify({
            'status': 'success',
            'message': 'Base de datos optimizada',
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error optimizando BD: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/backups', methods=['GET'])
@admin_required
def list_backups():
    """Listar todos los backups disponibles"""
    try:
        backup_stats = backup_manager.get_backup_stats()
        return jsonify(backup_stats)
    except Exception as e:
        logger.error(f"Error listando backups: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/backup/create', methods=['POST'])
@admin_required
def create_backup():
    """Crear backup manual"""
    try:
        backup = backup_manager.create_backup(backup_type='manual')
        if backup.get('status') == 'success':
            return jsonify(backup), 201
        else:
            return jsonify(backup), 500
    except Exception as e:
        logger.error(f"Error creando backup: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/backup/cleanup', methods=['POST'])
@admin_required
def cleanup_backups():
    """Limpiar backups antiguos"""
    try:
        result = backup_manager.cleanup_old_backups()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error limpiando backups: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/backup/restore/<backup_filename>', methods=['POST'])
@admin_required
def restore_backup(backup_filename):
    """Restaurar base de datos desde backup"""
    try:
        result = backup_manager.restore_backup(backup_filename)
        if result.get('status') == 'success':
            logger.warning(f"✅ Base de datos restaurada desde {backup_filename}")
            return jsonify(result)
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Error restaurando backup: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/imap/sync-all', methods=['POST'])
@token_required
def sync_all_emails():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM empresas WHERE activo = 1")
        empresas = [dict(row) for row in cur.fetchall()]
        
        results = []
        for emp in empresas:
            logger.info(f"Sincronizando {emp['nombre']}...")
            try:
                # Desencriptar contraseña
                password = decrypt_password(emp['email_pass'])
                
                # Conexión IMAP
                with imap_tools.MailBox(emp['imap_host'], port=emp['imap_port']).login(emp['email_user'], password, initial_folder='INBOX') as mailbox:
                    synced_count = 0
                    # Obtener los últimos 100 correos
                    for msg in mailbox.fetch(limit=100, reverse=True):
                        # Generar un thread_id único concatenando el email para evitar colisiones entre cuentas
                        raw_id = msg.uid or msg.message_id
                        tid = f"{emp['email_user']}_{raw_id}"
                        
                        # Insertar o ignorar si ya existe
                        cur.execute('''
                            INSERT OR IGNORE INTO hilos (
                                thread_id, remitente, asunto, mensaje, cuenta_empresa, 
                                correo_empresa, folder, fecha, adjuntos, estado_ticket
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            tid, msg.from_, msg.subject, msg.html or msg.text, 
                            emp['nombre'], emp['email_user'], 'INBOX', 
                            msg.date.strftime('%Y-%m-%d %H:%M:%S'), 
                            1 if msg.attachments else 0, 'PENDIENTE'
                        ))
                        if cur.rowcount > 0:
                            synced_count += 1
                    
                results.append({'empresa': emp['nombre'], 'synced': synced_count, 'success': True})
            except Exception as e:
                logger.error(f"Error sincronizando {emp['nombre']}: {e}")
                results.append({'empresa': emp['nombre'], 'error': str(e), 'success': False})
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'results': results, 'status': 'completed'})
    except Exception as e:
        logger.error(f"Error general en sync_all: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/settings', methods=['GET'])
@admin_required
def get_settings():
    """Obtener configuración del sistema"""
    return jsonify({
        'gemini_api_key_set': bool(config.GEMINI_API_KEY)
    })

@app.route('/api/admin/settings', methods=['POST'])
@admin_required
def update_settings():
    """Actualizar configuración del sistema"""
    data = request.json or {}
    
    if 'gemini_api_key' in data:
        new_key = data['gemini_api_key'].strip()
        if new_key:
            env_path = os.path.join(BASE_DIR, '.env')
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            updated = False
            new_lines = []
            for line in lines:
                if line.startswith('GEMINI_API_KEY='):
                    new_lines.append(f'GEMINI_API_KEY={new_key}\n')
                    updated = True
                else:
                    new_lines.append(line)
            
            if not updated:
                new_lines.append(f'GEMINI_API_KEY={new_key}\n')
            
            with open(env_path, 'w') as f:
                f.writelines(new_lines)
            
            config.GEMINI_API_KEY = new_key
            logger.info("✅ API Key de Gemini actualizada")
    
    return jsonify({'status': 'ok', 'message': 'Configuración actualizada'})

@app.route('/api/ai/generate-response', methods=['POST'])
@token_required
def generate_ai_response():
    """Generar respuesta automática con IA (Gemini)"""
    data = request.json or {}
    mensaje = data.get('mensaje', '').strip()
    asunto = data.get('asunto', '').strip()
    
    if not mensaje:
        return jsonify({'error': 'Se requiere el mensaje para generar respuesta'}), 400
    
    if not config.GEMINI_API_KEY:
        return jsonify({'error': 'API Key de Gemini no configurada'}), 500
    
    try:
        import requests
        
        prompt = f"""Eres un asistente de soporte al cliente profesional. Genera una respuesta automática y cortés al siguiente correo:

Asunto: {asunto}
Mensaje: {mensaje}

La respuesta debe ser:
- Profesional y amable
- Breve pero completa
- En español
- Lista para enviar (sin lugar para firma, el sistema la añadirá)

Respuesta:"""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={config.GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            'contents': [{'parts': [{'text': prompt}]}]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': ai_response, 'status': 'success'})
        else:
            logger.error(f"Error de Gemini API: {response.text}")
            return jsonify({'error': 'Error al generar respuesta con IA'}), 500
            
    except Exception as e:
        logger.error(f"Error en generate_ai_response: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    logger.info(f"🚀 Iniciando Agent Email AIRIS V1")
    logger.info(f"📍 Ambiente: {config.ENVIRONMENT}")
    logger.info(f"🔌 http://{config.HOST}:{config.PORT}")
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
