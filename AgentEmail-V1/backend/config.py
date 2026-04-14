"""
Configuración centralizada para Agent Email AIRIS V1
Gestiona environment variables, secrets y configuración por ambiente
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    
    # Directorios
    BASE_DIR = Path(__file__).resolve().parent.parent
    FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Crear directorio de logs si no existe
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Ambiente
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Servidor
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    WORKERS = int(os.getenv('WORKERS', 4 if ENVIRONMENT == 'production' else 2))
    
    # JWT & Seguridad
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY or SECRET_KEY.startswith('dev-'):
        raise ValueError(
            "⚠️  SECRET_KEY no configurado o inseguro. "
            "Ejecuta: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRE_HOURS = int(os.getenv('JWT_EXPIRE_HOURS', 24))
    JWT_EXPIRATION = timedelta(hours=JWT_EXPIRE_HOURS)
    
    # Base de Datos
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./database/agent_email.db')
    DB_PATH = os.path.join(DATABASE_DIR, 'agent_email.db')
    DB_TIMEOUT = int(os.getenv('DB_TIMEOUT', 5))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(LOGS_DIR, 'agent-email.log'))
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10 MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # CORS
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000'
    ).split(',')
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    
    # Encriptación
    ENCRYPTION_KEY_FILE = os.getenv('ENCRYPTION_KEY_FILE', os.path.join(BASE_DIR, '.key'))
    
    # IMAP/SMTP Timeouts
    IMAP_TIMEOUT = int(os.getenv('IMAP_TIMEOUT', 30))
    SMTP_TIMEOUT = int(os.getenv('SMTP_TIMEOUT', 30))
    
    @classmethod
    def validate(cls):
        """Valida configuración crítica"""
        critical_fields = [
            ('SECRET_KEY', cls.SECRET_KEY),
            ('DATABASE_DIR', cls.DATABASE_DIR),
            ('LOGS_DIR', cls.LOGS_DIR),
        ]
        
        for field_name, field_value in critical_fields:
            if not field_value:
                raise ValueError(f"Configuración crítica faltante: {field_name}")
        
        return True


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    ENVIRONMENT = 'development'
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Configuración para producción"""
    ENVIRONMENT = 'production'
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'
    WORKERS = 4
    
    @classmethod
    def validate(cls):
        """En producción, requiere validaciones extras"""
        super().validate()
        
        if cls.DEBUG:
            raise ValueError("⚠️  DEBUG no debe estar habilitado en producción")
        
        if 'dev-secret-key' in (cls.SECRET_KEY or '').lower():
            raise ValueError("⚠️  No uses SECRET_KEY de desarrollo en producción")
        
        return True


class TestingConfig(Config):
    """Configuración para testing"""
    ENVIRONMENT = 'testing'
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    LOG_LEVEL = 'DEBUG'


def get_config():
    """Retorna la configuración apropiada según ENVIRONMENT"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    config_class.validate()
    return config_class


# Instancia global de configuración
config = get_config()
