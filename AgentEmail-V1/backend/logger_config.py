"""
Configuración de logging estructurado
Soporta archivos rotados, niveles dinámicos y formato consistente
"""

import logging
import logging.handlers
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger
from config import config


class JsonFormatter(jsonlogger.JsonFormatter):
    """Formateador JSON personalizado para logs estructurados"""
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Agregar timestamp ISO
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['environment'] = config.ENVIRONMENT


def setup_logging():
    """Configura logging centralizado con archivos rotados"""
    
    # Logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Remover handlers anteriores si existen
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Formato para consola
    console_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    root_logger.addHandler(console_handler)
    
    # Handler para archivo (rotado)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=config.LOG_FILE,
            maxBytes=config.LOG_MAX_BYTES,
            backupCount=config.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_formatter = JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
    except Exception as e:
        root_logger.warning(f"No se pudo configurar file handler: {e}")
    
    return root_logger


# Configurar logs al importar
logger = setup_logging()
