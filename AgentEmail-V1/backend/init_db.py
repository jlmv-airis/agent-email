"""
Database Initialization Script
Inicializa base de datos con tablas y datos por defecto
"""

import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from config import config
from logger_config import logger
from database import db_manager
from backup_manager import backup_manager


def init_database():
    """Inicializar base de datos SQLite con estructura completa"""
    
    db_path = Path(config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    is_new_db = not db_path.exists()
    
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    
    if is_new_db:
        logger.info("📋 Creando estructura de base de datos...")
    else:
        logger.info("📋 Verificando/Actualizando base de datos...")
    
    # Tabla usuarios
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de secretos TOTP (2FA)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS totp_secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            secret TEXT NOT NULL,
            enabled INTEGER DEFAULT 0,
            backup_codes TEXT,
            last_used TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabla empresas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            alias TEXT,
            imap_host TEXT,
            imap_port INTEGER DEFAULT 993,
            email_user TEXT UNIQUE,
            email_pass TEXT,
            smtp_host TEXT,
            smtp_port INTEGER DEFAULT 465,
            logo_url TEXT,
            activo INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla hilos (threads de emails)
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de auditoría (para rastrear cambios)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tabla TEXT NOT NULL,
            accion TEXT NOT NULL,
            registro_id INTEGER,
            cambios TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Índices para hilos
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_folder ON hilos(folder)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_empresa_folder_fecha ON hilos(cuenta_empresa, folder, fecha)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_thread_id ON hilos(thread_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_correo_empresa ON hilos(correo_empresa)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_estado_ticket ON hilos(estado_ticket)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_asignado_a ON hilos(asignado_a)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_fecha ON hilos(fecha)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_hilos_leido ON hilos(leido)")
    
    # Índices para usuarios
    cur.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON usuarios(activo)")
    
    # Índices para totp_secrets
    cur.execute("CREATE INDEX IF NOT EXISTS idx_totp_user_id ON totp_secrets(user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_totp_enabled ON totp_secrets(enabled)")
    
    # Índices para empresas
    cur.execute("CREATE INDEX IF NOT EXISTS idx_empresas_email_user ON empresas(email_user)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_empresas_activo ON empresas(activo)")
    
    # Tabla de etiquetas personalizadas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS etiquetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            color TEXT NOT NULL,
            descripcion TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(created_by) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabla de relación hilos-etiquetas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hilos_etiquetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hilo_id INTEGER NOT NULL,
            etiqueta_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(hilo_id) REFERENCES hilos(id),
            FOREIGN KEY(etiqueta_id) REFERENCES etiquetas(id)
        )
    ''')
    
    # Tabla de borradores
    cur.execute('''
        CREATE TABLE IF NOT EXISTS borradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hilo_id INTEGER,
            destinatario TEXT,
            cc TEXT,
            bcc TEXT,
            asunto TEXT,
            cuerpo TEXT,
            cuenta_empresa TEXT,
            email_user TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(hilo_id) REFERENCES hilos(id),
            FOREIGN KEY(created_by) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabla de programación de envíos
    cur.execute('''
        CREATE TABLE IF NOT EXISTS envios_programados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hilo_id INTEGER,
            destinatario TEXT,
            asunto TEXT,
            cuerpo TEXT,
            fecha_programada TIMESTAMP NOT NULL,
            created_by INTEGER,
            estado TEXT DEFAULT 'pendiente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(hilo_id) REFERENCES hilos(id),
            FOREIGN KEY(created_by) REFERENCES usuarios(id)
        )
    ''')
    
    # Crear usuario admin por defecto
    cur.execute("SELECT id FROM usuarios WHERE username = 'admin' LIMIT 1")
    if not cur.fetchone():
        password_hash = generate_password_hash('admin')
        cur.execute('''
            INSERT INTO usuarios (username, nombre, email, password_hash, rol, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', 'Administrador', 'admin@airis.com', password_hash, 'admin', 'Cuenta de administrador principal'))
        logger.info("✅ Usuario admin creado")
    
    conn.commit()
    cur.close()
    conn.close()
    
    # Aplicar optimizaciones
    logger.info("🔧 Aplicando optimizaciones de base de datos...")
    db_manager.ensure_indexes()
    db_manager.analyze_database()
    
    if is_new_db:
        logger.info("✅ Base de datos inicializada correctamente")
    else:
        logger.info("✅ Base de datos verificada y actualizada")


def backup_before_migration():
    """Crear backup antes de migración"""
    logger.info("💾 Creando backup de seguridad antes de migración...")
    backup_info = backup_manager.create_backup(backup_type='pre-migration')
    logger.info(f"✅ Backup creado: {backup_info.get('filename')}")
    return backup_info


if __name__ == '__main__':
    init_database()
