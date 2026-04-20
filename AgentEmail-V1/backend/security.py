"""
Security Module - Headers, CORS, Rate Limiting, Input Validation
Centraliza todas las medidas de seguridad de la aplicación
"""

from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import re
from config import config
from logger_config import logger


class SecurityManager:
    """Gestor centralizado de seguridad"""
    
    def __init__(self, app=None):
        self.app = app
        self.limiter = None
        
    def init_app(self, app):
        """Inicializar medidas de seguridad en Flask app"""
        self.app = app
        
        # Configurar rate limiting
        if config.RATE_LIMIT_ENABLED:
            self.limiter = Limiter(
                app=app,
                key_func=get_remote_address,
                default_limits=[f"{config.RATE_LIMIT_PER_MINUTE}/minute"],
                storage_uri="memory://",  # Cambiar a redis:// en producción
                strategy="fixed-window"
            )
            logger.info("✅ Rate limiting habilitado")
        else:
            self.limiter = None
            logger.info("⚠️  Rate limiting deshabilitado (development)")
        
        # Agregar security headers middleware
        @app.after_request
        def set_security_headers(response):
            # Prevenir clickjacking
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            
            # Prevenir MIME type sniffing
            response.headers['X-Content-Type-Options'] = 'nosniff'
            
            # Habilitar XSS protection (deprecated pero aún util)
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
            # Content Security Policy
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' wss: https:; "
                "frame-ancestors 'self';"
            )
            
            # Referrer Policy
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Permissive Policy (evita errores de features como micrófono, cámara)
            response.headers['Permissions-Policy'] = (
                'geolocation=(), '
                'microphone=(), '
                'camera=(), '
                'payment=(), '
                'usb=(), '
                'magnetometer=(), '
                'gyroscope=(), '
                'accelerometer=()'
            )
            
            return response
        
        logger.info("✅ Security headers configurados")
    
    def require_rate_limit(self, limit=None):
        """Decorador para aplicar rate limiting a rutas específicas"""
        def decorator(f):
            if self.limiter:
                rate_limit = limit or f"{config.RATE_LIMIT_PER_MINUTE}/minute"
                return self.limiter.limit(rate_limit)(f)
            return f
        return decorator


class InputValidator:
    """Validaciones de input estructuradas"""
    
    # Patrones de validación
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'username': r'^[a-zA-Z0-9_-]{3,32}$',
        'url': r'^https?://[^\s/$.?#].[^\s]*$',
        'alphanumeric': r'^[a-zA-Z0-9]+$',
        'uuid': r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
        'thread_id': r'^[a-zA-Z0-9_\-\.]+_[a-zA-Z0-9]+$',
    }
    
    # Límites de longitud
    LENGTH_LIMITS = {
        'email': 254,
        'username': 32,
        'password': 255,
        'nombre': 100,
        'asunto': 255,
        'mensaje': 50000,
        'url': 2048,
    }
    
    # Caracteres prohibidos
    FORBIDDEN_CHARS = {
        'username': ['<', '>', '"', "'", '&', ';', '%', '\\'],
        'default': ['<script', '<?php', 'javascript:', 'on', '->'],
    }
    
    @classmethod
    def validate_email(cls, email):
        """Validar email"""
        if not email:
            return False, "Email requerido"
        if len(email) > cls.LENGTH_LIMITS['email']:
            return False, f"Email muy largo (máx {cls.LENGTH_LIMITS['email']} caracteres)"
        if not re.match(cls.PATTERNS['email'], email):
            return False, "Email inválido"
        return True, "OK"
    
    @classmethod
    def validate_username(cls, username):
        """Validar username"""
        if not username:
            return False, "Username requerido"
        if len(username) > cls.LENGTH_LIMITS['username']:
            return False, f"Username muy largo (máx {cls.LENGTH_LIMITS['username']} caracteres)"
        if not re.match(cls.PATTERNS['username'], username):
            return False, "Username debe contener números, letras, guión o guión bajo"
        
        # Verificar caracteres prohibidos
        for char in cls.FORBIDDEN_CHARS['username']:
            if char in username.lower():
                return False, f"Username contiene carácter prohibido: {char}"
        
        return True, "OK"
    
    @classmethod
    def validate_password(cls, password, min_length=8):
        """Validar password"""
        if not password:
            return False, "Password requerido"
        if len(password) < min_length:
            return False, f"Password debe tener al menos {min_length} caracteres"
        if len(password) > cls.LENGTH_LIMITS['password']:
            return False, f"Password muy largo (máx {cls.LENGTH_LIMITS['password']} caracteres)"
        
        # Criterios mínimos de fuerza
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?' for c in password)
        
        # En development, permitir passwords simples; en producción, requerir más complejidad
        if config.ENVIRONMENT == 'production':
            strength = sum([has_upper, has_lower, has_digit, has_special])
            if strength < 3:
                return False, "Password debe contener mayúsculas, minúsculas, números y caracteres especiales"
        
        return True, "OK"
    
    @classmethod
    def validate_thread_id(cls, thread_id):
        """Validar thread_id"""
        if not thread_id:
            return False, "thread_id requerido"
        if len(thread_id) > 255:
            return False, "thread_id muy largo"
        if not re.match(cls.PATTERNS['thread_id'], thread_id):
            return False, "Formato de thread_id inválido"
        return True, "OK"
    
    @classmethod
    def sanitize_string(cls, value, field_type='default'):
        """Limpiar strings de caracteres peligrosos"""
        if not isinstance(value, str):
            return value
        
        value = ' '.join(value.split())
        
        forbidden = cls.FORBIDDEN_CHARS.get(field_type, cls.FORBIDDEN_CHARS['default'])
        for char in forbidden:
            value = value.replace(char, '')
        
        return value
    
    @classmethod
    def sanitize_html(cls, html_content, allow_images=True):
        """Sanitizar contenido HTML para prevenir XSS"""
        if not isinstance(html_content, str):
            return html_content
        
        import re
        
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        html_content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        html_content = re.sub(r'javascript:', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'on\w+\s*=', '', html_content, flags=re.IGNORECASE)
        
        if not allow_images:
            html_content = re.sub(r'<img[^>]*>', '', html_content, flags=re.IGNORECASE)
        
        html_content = re.sub(r'<object[^>]*>.*?</object>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        html_content = re.sub(r'<embed[^>]*>', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<link[^>]*>', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'@import', '', html_content, flags=re.IGNORECASE)
        
        if 'data:' in html_content.lower():
            html_content = re.sub(r'data:[^<>]*base64,[a-zA-Z0-9+/=]+', '[FILTERED]', html_content, flags=re.IGNORECASE)
        
        return html_content
    
    @classmethod
    def validate_input_length(cls, value, field_name='campo', max_length=1000):
        """Validar longitud de input"""
        if not isinstance(value, str):
            return True, "OK"
        
        if len(value) > max_length:
            return False, f"{field_name} muy largo (máx {max_length} caracteres)"
        
        return True, "OK"
    
    @classmethod
    def validate_json_request(cls, data, required_fields, field_types=None):
        """Validar estructura de request JSON"""
        if field_types is None:
            field_types = {}
        
        if not isinstance(data, dict):
            return False, "Datos deben ser un JSON object"
        
        # Verificar campos requeridos
        missing = [f for f in required_fields if f not in data or data[f] is None]
        if missing:
            return False, f"Campos requeridos faltantes: {', '.join(missing)}"
        
        # Verificar tipos
        for field, expected_type in field_types.items():
            if field in data and data[field] is not None:
                if not isinstance(data[field], expected_type):
                    return False, f"Campo '{field}' debe ser tipo {expected_type.__name__}"
        
        return True, "OK"


def require_api_key(f):
    """Decorador para requerir API key en headers (opcional, para futuro)"""
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return {'error': 'API key requerida'}, 401
        # Validar contra keys permitidas (en producción, consultar DB)
        return f(*args, **kwargs)
    return decorated


# Instancia global
security = SecurityManager()
validator = InputValidator()
