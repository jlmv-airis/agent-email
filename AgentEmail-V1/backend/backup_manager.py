"""
Backup Manager - Sistema de backups automáticos y manuales
Gestiona copias de seguridad de base de datos
"""

import sqlite3
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from config import config
from logger_config import logger


class BackupManager:
    """Gestor de backups SQLite"""
    
    def __init__(self, backup_dir=None):
        self.backup_dir = backup_dir or os.path.join(config.BASE_DIR, 'backups')
        self.db_path = config.DB_PATH
        self.max_backups = 10  # Mantener últimos 10 backups
        self.retention_days = 30  # Borrar backups más antiguos de 30 días
        
        # Crear directorio de backups si no existe
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_type='manual'):
        """
        Crear backup de base de datos
        
        Args:
            backup_type: 'manual', 'scheduled', 'daily'
        
        Returns:
            dict con información del backup creado
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"agent_email_{backup_type}_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            # Usar SQLite backup mechanism
            source_conn = sqlite3.connect(self.db_path)
            backup_conn = sqlite3.connect(backup_path)
            
            with backup_conn:
                source_conn.backup(backup_conn)
            
            source_conn.close()
            backup_conn.close()
            
            # Obtener info del backup
            backup_size = os.path.getsize(backup_path)
            
            backup_info = {
                'filename': backup_filename,
                'path': backup_path,
                'type': backup_type,
                'timestamp': timestamp,
                'size_bytes': backup_size,
                'size_mb': round(backup_size / (1024 * 1024), 2),
                'status': 'success'
            }
            
            logger.info(f"✅ Backup creado: {backup_filename} ({backup_info['size_mb']} MB)")
            return backup_info
        
        except Exception as e:
            logger.error(f"❌ Error creando backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def list_backups(self):
        """Listar todos los backups disponibles"""
        backups = []
        
        try:
            for filename in sorted(os.listdir(self.backup_dir), reverse=True):
                if filename.endswith('.db'):
                    filepath = os.path.join(self.backup_dir, filename)
                    size = os.path.getsize(filepath)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    backups.append({
                        'filename': filename,
                        'path': filepath,
                        'size_mb': round(size / (1024 * 1024), 2),
                        'created_at': mtime.isoformat(),
                        'age_hours': round((datetime.now() - mtime).total_seconds() / 3600, 1)
                    })
        except Exception as e:
            logger.error(f"Error listando backups: {e}")
        
        return backups
    
    def cleanup_old_backups(self):
        """Limpiar backups antiguos (por edad y cantidad)"""
        backups = self.list_backups()
        
        if not backups:
            return {'status': 'ok', 'cleaned': 0}
        
        cleaned_count = 0
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        # Obtener backups para eliminar
        to_remove = []
        
        # Por antigüedad
        for backup in backups:
            backup_date = datetime.fromisoformat(backup['created_at'])
            if backup_date < cutoff_date:
                to_remove.append(backup)
        
        # Por cantidad (mantener solo últimos max_backups)
        if len(backups) > self.max_backups:
            to_remove.extend(backups[self.max_backups:])
        
        # Eliminar duplicados
        to_remove = list({b['filename']: b for b in to_remove}.values())
        
        # Ejecutar eliminación
        for backup in to_remove:
            try:
                os.remove(backup['path'])
                logger.info(f"🗑️  Backup eliminado: {backup['filename']}")
                cleaned_count += 1
            except Exception as e:
                logger.error(f"Error eliminando {backup['filename']}: {e}")
        
        return {
            'status': 'ok',
            'cleaned': cleaned_count,
            'remaining_backups': len(backups) - cleaned_count
        }
    
    def restore_backup(self, backup_filename):
        """
        Restaurar base de datos desde backup
        CUIDADO: Reemplazará la base de datos actual
        """
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            return {'status': 'error', 'message': 'Backup no encontrado'}
        
        try:
            # Crear backup de seguridad de la BD actual
            current_backup = f"before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(self.db_path, os.path.join(self.backup_dir, current_backup))
            
            # Restaurar desde backup
            shutil.copy2(backup_path, self.db_path)
            
            logger.warning(f"⚠️  Base de datos restaurada desde {backup_filename}")
            return {
                'status': 'success',
                'message': f'Restaurado desde {backup_filename}',
                'safety_backup': current_backup
            }
        except Exception as e:
            logger.error(f"Error restaurando backup: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_backup_stats(self):
        """Obtener estadísticas de backups"""
        backups = self.list_backups()
        
        total_size = sum(b['size_mb'] for b in backups)
        
        return {
            'total_backups': len(backups),
            'total_size_mb': round(total_size, 2),
            'oldest_backup': backups[-1]['created_at'] if backups else None,
            'newest_backup': backups[0]['created_at'] if backups else None,
            'backup_dir': self.backup_dir,
            'backups': backups
        }


# Instancia global
backup_manager = BackupManager()
