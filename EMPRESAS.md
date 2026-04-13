# Empresas Configuradas - Agent Email AIRIS

Este archivo es una referencia de las empresas configuradas en el sistema.

## ⚠️ Importante - Seguridad

Las contraseñas NUNCA deben almacenarse en texto plano. El sistema usa:
- **Cifrado Fernet** para almacenar en la base de datos SQLite
- **API del Panel** para gestionar credenciales de forma segura

---

## Empresas Registradas

| ID | Nombre | Alias | Host IMAP | Puerto | Email |
|----|--------|-------|-----------|--------|-------|
| 1 | PlatinoServicios | PlatiCoMx-02 | mail.platinoservicios.com | 993 | administracion@platinoservicios.com |
| 2 | All4Store | StoreMex-02 | mail.all4store.com.mx | 993 | ejecutivo.logistica@all4store.com.mx |

---

## Cómo Agregar Nueva Empresa

### Método 1: Desde el Panel (Recomendado)

1. Abre **http://localhost:8000/Panel.html**
2. Ve a **Configuración → Empresas**
3. Click en **"+ Nueva Empresa"**
4. Completa los datos:
   - **Nombre:** Nombre de la empresa
   - **Alias:** Identificador corto
   - **IMAP Host:**Servidor de correo (ej: mail.dominio.com)
   - **IMAP Puerto:** 993 (estándar) o 995
   - **Email Usuario:** correo@dominio.com
   - **Contraseña:** ******
5. Click en **Guardar**
6. Click en **Sincronizar** para probar conexión

### Método 2: Directamente en n8n

1. Ve a **http://localhost:5678**
2. Importar workflow existente
3. Duplicar nodo IMAP
4. Actualizar credenciales
5. Activar workflow

---

## Configuración IMAP Común

| Proveedor | Host IMAP | Puerto | Host SMTP | Puerto |
|----------|-----------|--------|----------|---------|
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 465 |
| Outlook | outlook.office365.com | 993 | smtp.office365.com | 587 |
| Yahoo | imap.mail.yahoo.com | 993 | smtp.mail.yahoo.com | 465 |
| Zoho Mail | imap.zoho.com | 993 | smtp.zoho.com | 465 |
| Hosting cPanel | mail.dominio.com | 993 | mail.dominio.com | 465 |

---

##Última Actualización
- Fecha: 13 de abril de 2026
- Versión: v0.1.0