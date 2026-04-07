import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://n8n_user:n8n_password@localhost:5432/n8n_db')
N8N_URL = os.environ.get('N8N_URL', 'http://localhost:5678')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                nombre VARCHAR(100),
                email VARCHAR(255),
                password_hash VARCHAR(255),
                rol VARCHAR(20) DEFAULT 'operador',
                notas TEXT,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS empresas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                alias VARCHAR(100),
                imap_host VARCHAR(255),
                imap_port INTEGER DEFAULT 993,
                email_user VARCHAR(255),
                email_pass VARCHAR(255),
                smtp_host VARCHAR(255),
                smtp_port INTEGER DEFAULT 465,
                logo_url TEXT,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute("SELECT id FROM usuarios WHERE username = 'admin' LIMIT 1")
        if not cur.fetchone():
            password_hash = generate_password_hash('admin')
            cur.execute('''
                INSERT INTO usuarios (username, nombre, email, password_hash, rol, notas)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', ('admin', 'Administrador', 'admin@airis.com', password_hash, 'admin', 'Cuenta principal'))
            logger.info("Usuario admin creado")
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error inicializando DB: {e}")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/Panel.html')
def panel():
    return send_file('Panel.html')

@app.route('/login.html')
def login():
    return send_file('login.html')

@app.route('/api/status')
def status():
    try:
        conn = get_db_connection()
        conn.close()
        db_status = 'connected'
    except:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'n8n_url': N8N_URL,
        'version': '1.2'
    })

@app.route('/api/config')
def get_all_config():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT clave, valor FROM configuracion')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        config = {row['clave']: row['valor'] for row in rows}
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        empresas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(row) for row in empresas])
    except Exception as e:
        logger.error(f"Error get_empresas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas', methods=['POST'])
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['nombre'],
            data.get('alias', ''),
            data.get('imap_host', 'imap.gmail.com'),
            data.get('imap_port', 993),
            data['email_user'],
            data.get('email_pass', ''),
            data.get('smtp_host', data.get('imap_host', '')),
            data.get('smtp_port', 465),
            data.get('logo_url', '')
        ))
        
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': new_id, 'message': 'Empresa creada correctamente'}), 201
    except Exception as e:
        logger.error(f"Error create_empresa: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/<int:empresa_id>', methods=['PUT'])
def update_empresa(empresa_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_fields = []
        params = []
        
        for field in ['nombre', 'alias', 'imap_host', 'imap_port', 'email_user', 'smtp_host', 'smtp_port', 'logo_url']:
            if field in data:
                update_fields.append(f'{field} = %s')
                params.append(data[field])
        
        if 'email_pass' in data and data['email_pass']:
            update_fields.append('email_pass = %s')
            params.append(data['email_pass'])
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        params.append(empresa_id)
        
        cur.execute(f'''
            UPDATE empresas SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id
        ''', params)
        
        result = cur.fetchone()
        if not result:
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
def delete_empresa(empresa_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM empresas WHERE id = %s RETURNING id', (empresa_id,))
        result = cur.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'error': 'Empresa no encontrada'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Empresa eliminada correctamente'})
    except Exception as e:
        logger.error(f"Error delete_empresa: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores', methods=['GET'])
def get_operadores():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, username, nombre, email, rol, notas, activo, created_at 
            FROM usuarios 
            WHERE activo = TRUE 
            ORDER BY created_at DESC
        ''')
        operadores = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(row) for row in operadores])
    except Exception as e:
        logger.error(f"Error get_operadores: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores', methods=['POST'])
def create_operador():
    data = request.json
    required = ['username', 'nombre', 'email']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Campo requerido: {field}'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT id FROM usuarios WHERE username = %s', (data['username'],))
        if cur.fetchone():
            conn.close()
            return jsonify({'error': 'El username ya existe'}), 400
        
        password_hash = generate_password_hash(data.get('password', 'temp123'))
        
        cur.execute('''
            INSERT INTO usuarios (username, nombre, email, password_hash, rol, notas)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['username'],
            data['nombre'],
            data['email'],
            password_hash,
            data.get('rol', 'operador'),
            data.get('notas', '')
        ))
        
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': new_id, 'message': 'Operador creado correctamente'}), 201
    except Exception as e:
        logger.error(f"Error create_operador: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/operadores/<username>', methods=['PUT'])
def update_operador(username):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_fields = []
        params = []
        
        for field in ['nombre', 'email', 'rol', 'notas']:
            if field in data:
                update_fields.append(f'{field} = %s')
                params.append(data[field])
        
        if 'password' in data and data['password']:
            update_fields.append('password_hash = %s')
            params.append(generate_password_hash(data['password']))
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        params.append(username)
        
        cur.execute(f'''
            UPDATE usuarios SET {', '.join(update_fields)}
            WHERE username = %s AND username != 'admin'
            RETURNING id
        ''', params)
        
        result = cur.fetchone()
        if not result:
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
def delete_operador(username):
    if username == 'admin':
        return jsonify({'error': 'No se puede eliminar al administrador'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            UPDATE usuarios SET activo = FALSE 
            WHERE username = %s AND username != 'admin'
            RETURNING id
        ''', (username,))
        
        result = cur.fetchone()
        if not result:
            conn.close()
            return jsonify({'error': 'Operador no encontrado'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Operador eliminado correctamente'})
    except Exception as e:
        logger.error(f"Error delete_operador: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/<key>', methods=['GET', 'PUT'])
def config(key):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == 'GET':
            cur.execute('SELECT valor FROM configuracion WHERE clave = %s', (key,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return jsonify({'valor': result['valor'] if result else None})
        
        else:
            data = request.json
            cur.execute('''
                INSERT INTO configuracion (clave, valor) VALUES (%s, %s)
                ON CONFLICT (clave) DO UPDATE SET valor = EXCLUDED.valor
            ''', (key, data['valor']))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Configuración guardada'})
            
    except Exception as e:
        logger.error(f"Error config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
