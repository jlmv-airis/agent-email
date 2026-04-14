"""
Health Check Endpoints
Monitoreo de salud de la aplicación
"""

import sqlite3
from datetime import datetime
from config import config
from logger_config import logger


class HealthChecker:
    """Monitor de salud de la aplicación"""
    
    @staticmethod
    def check_database():
        """Verificar conexión a base de datos"""
        try:
            conn = sqlite3.connect(config.DB_PATH, timeout=config.DB_TIMEOUT)
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            conn.close()
            return True, "OK"
        except Exception as e:
            logger.error(f"Health check DB failed: {e}")
            return False, str(e)
    
    @staticmethod
    def check_configuration():
        """Verificar que configuración es válida"""
        try:
            critical = [
                ('SECRET_KEY', config.SECRET_KEY),
                ('DATABASE_PATH', config.DB_PATH),
                ('LOGS_DIR', config.LOGS_DIR),
            ]
            
            for name, value in critical:
                if not value:
                    return False, f"Config incompleta: {name}"
            
            return True, "OK"
        except Exception as e:
            logger.error(f"Health check config failed: {e}")
            return False, str(e)
    
    @staticmethod
    def get_health_status():
        """Obtener estado general de salud"""
        from flask import jsonify
        
        db_ok, db_msg = HealthChecker.check_database()
        config_ok, config_msg = HealthChecker.check_configuration()
        
        overall = "healthy" if (db_ok and config_ok) else "degraded"
        
        status = {
            'status': overall,
            'timestamp': datetime.utcnow().isoformat(),
            'environment': config.ENVIRONMENT,
            'checks': {
                'database': {
                    'status': 'pass' if db_ok else 'fail',
                    'message': db_msg
                },
                'configuration': {
                    'status': 'pass' if config_ok else 'fail',
                    'message': config_msg
                }
            },
            'version': '1.0.4',
            'uptime_seconds': None  # Implementar si es necesario
        }
        
        return status, 200 if overall == "healthy" else 503


def get_health_response():
    """Función auxiliar para retornar health check como JSON"""
    status, code = HealthChecker.get_health_status()
    return {
        'health': status,
        'code': code
    }
