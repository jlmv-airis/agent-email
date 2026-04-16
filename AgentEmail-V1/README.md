# 📧 Agent Email AIRIS - Versión V1.0.9

Este es el sistema SaaS unificado de gestión de correos electrónicos. Se ha refactorizado para eliminar dependencias externas (como n8n) y utilizar una arquitectura limpia de **Python (Flask) + SQLite**.

## 📌 Estado Actual del Proyecto
- **Versión:** v1.0.9
- **Acceso:** [http://localhost:8000](http://localhost:8000) (Se requiere login).
- **Flujo:** Login ➔ Redirección a Dashboard (index.html).

## 📁 Estructura de Archivos
- `/backend`: Servidor Flask (`server.py`) y llave de cifrado (`.key`).
- `/frontend`: Interfaz de usuario (`login.html` e `index.html`).
- `/database`: Base de datos local SQLite (`agent_email.db`).
- `/docs`: Documentación detallada y registro de empresas.

## 🔐 Credenciales por Defecto
- **Email:** `admin@airis.com`
- **Contraseña:** `admin123` (Verificada)

## ✅ Hitos Alcanzados (Versión 1.0.9)
- [x] **Interfaz Inspector Estilo Gmail:** Implementación del rediseño visual de la ventana de visualización de correos para que se asemeje a la interfaz de Gmail, con énfasis en legibilidad y estilo moderno.

## 🚀 Próximos Pasos (V1.0.9)
1. **Sistema de Etiquetas Dinámico:** Detección automática de etiquetas (Urgente, Soporte, etc.) basada en el contenido y visualización de badges de colores.
2. **Delegación de Tickets:** Implementar la lógica del backend para el endpoint de asignación de operadores.
3. **Exportación:** Implementar la descarga de reportes en PDF o Excel desde el Dashboard.
4. **Modo Oscuro/Claro:** Garantizar consistencia absoluta en el tema visual.

---
**Última actualización:** miércoles, 15 de abril de 2026.
**Objetivo:** Mantener el código en `index.html` como la única fuente de verdad para el panel administrativo.
