"""
Database Management Module
Gestiona índices, migraciones y optimizaciones de base de datos
"""

import sqlite3
import os
from datetime import datetime
from config import config
from logger_config import logger


class DatabaseManager:
    """Gestor de base de datos SQLite con optimizaciones"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or config.DB_PATH
    
    def get_connection(self):
        """Obtener conexión a base de datos"""
        conn = sqlite3.connect(self.db_path, timeout=config.DB_TIMEOUT)
        conn.row_factory = sqlite3.Row
        # Habilitar FK constraints
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def ensure_indexes(self):
        """Crear índices para optimización de queries"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        indexes = [
            # Tabla usuarios
            ("idx_usuarios_email", "usuarios", "email"),
            ("idx_usuarios_username", "usuarios", "username"),
            ("idx_usuarios_activo", "usuarios", "activo"),
            
            # Tabla empresas
            ("idx_empresas_email_user", "empresas", "email_user"),
            ("idx_empresas_activo", "empresas", "activo"),
            
            # Tabla hilos - Los más críticos
            ("idx_hilos_thread_id", "hilos", "thread_id"),
            ("idx_hilos_correo_empresa", "hilos", "correo_empresa"),
            ("idx_hilos_estado_ticket", "hilos", "estado_ticket"),
            ("idx_hilos_asignado_a", "hilos", "asignado_a"),
            ("idx_hilos_fecha", "hilos", "fecha DESC"),
            ("idx_hilos_folder", "hilos", "folder"),
            ("idx_hilos_leido", "hilos", "leido"),

            # Índices compuestos para queries comunes
            ("idx_hilos_empresa_estado", "hilos", "cuenta_empresa, estado_ticket"),
            ("idx_hilos_empresa_fecha", "hilos", "correo_empresa, fecha DESC"),
            ]
        for idx_name, table, columns in indexes:
            try:
                # Verificar si el índice ya existe
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='index' AND name=?",
                    (idx_name,)
                )
                if cur.fetchone():
                    logger.debug(f"Índice {idx_name} ya existe")
                    continue
                
                create_stmt = f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({columns})"
                cur.execute(create_stmt)
                logger.info(f"✅ Índice creado: {idx_name}")
            except sqlite3.Error as e:
                logger.error(f"Error creando índice {idx_name}: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Optimización de índices completada")
    
    def analyze_database(self):
        """Ejecutar ANALYZE para actualizar estadísticas de tabla"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("ANALYZE")
            conn.commit()
            logger.info("✅ ANALYZE completado (estadísticas de tabla actualizadas)")
        except sqlite3.Error as e:
            logger.error(f"Error en ANALYZE: {e}")
        finally:
            cur.close()
            conn.close()
    
    def vacuum_database(self):
        """Limpiar y optimizar archivo de BD"""
        conn = self.get_connection()
        
        try:
            conn.execute("VACUUM")
            logger.info("✅ VACUUM completado (BD compactada)")
        except sqlite3.Error as e:
            logger.error(f"Error en VACUUM: {e}")
        finally:
            conn.close()
    
    def get_database_stats(self):
        """Obtener estadísticas de la base de datos"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        stats = {}
        
        # Tamaño del archivo
        try:
            size_bytes = os.path.getsize(self.db_path)
            stats['file_size_bytes'] = size_bytes
            stats['file_size_mb'] = round(size_bytes / (1024 * 1024), 2)
        except:
            stats['file_size_mb'] = 0
        
        # Contar registros por tabla
        try:
            cur.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            tables = cur.fetchall()
            
            stats['tables'] = {}
            for (table_name,) in tables:
                cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cur.fetchone()[0]
                stats['tables'][table_name] = count
        except sqlite3.Error as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
        
        cur.close()
        conn.close()
        
        return stats
    
    def optimize_all(self):
        """Ejecutar todas las optimizaciones"""
        logger.info("🔧 Iniciando optimización completa de BD...")
        
        self.ensure_indexes()
        self.analyze_database()
        self.vacuum_database()
        
        stats = self.get_database_stats()
        logger.info(f"📊 Estadísticas: {stats}")
        
        return stats
    
    def backup_database(self, backup_dir=None):
        """Crear backup manual de base de datos"""
        from backup_manager import BackupManager
        
        backup_dir = backup_dir or os.path.join(config.BASE_DIR, 'backups')
        bm = BackupManager(backup_dir)
        return bm.create_backup()


# Instancia global
db_manager = DatabaseManager()
