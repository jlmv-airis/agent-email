# 📧 Agent Email AIRIS - Versión V1

Este es el sistema SaaS unificado de gestión de correos electrónicos. Se ha refactorizado para eliminar dependencias externas (como n8n) y utilizar una arquitectura limpia de **Python (Flask) + SQLite**.

## 📌 Estado Actual del Proyecto
- **Fase:** v0.1.0 (Analytics y Notificaciones) - **REFACTORIZADA V1**.
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

## ✅ Hitos Alcanzados (V1)
- [x] **Refactorización completa:** Eliminado n8n, API 100% nativa en Python (Flask).
- [x] **Sistema de Login:** Autenticación JWT verificada y operativa.
- [x] **Estructura V1:** Organización de carpetas (backend, frontend, database, docs) consolidada.
- [x] **Dashboard:** Gráficos y métricas funcionales con Chart.js.
- [x] **Carga de Datos:** Visualización de cuentas webmail y hilos de correo restaurada y verificada.
- [x] **Optimización:** Limpieza de errores de consola (TypeError null) y redirección automática de sesión.
- [x] **UI Sidebar:** Refinado con CSS estándar para asegurar alineación (padding-left: 40px) y márgenes elegantes, superando limitaciones de Tailwind CDN.
- [x] **Interactividad:** Lógica de redimensionamiento (Resizer) funcional, permitiendo ajustar el ancho del panel dinámicamente.
- [x] **Estabilidad Frontend:** Eliminación total de lógica de login heredada en `index.html`, erradicando los errores `TypeError` de consola.
- [x] **Checkpoint V1.1:** Interfaz "Apple Pro" validada visualmente mediante capturas y funcionalmente mediante navegación.
- [x] **Gestión de Buzones:** Implementada la visualización de carpetas (Entrada, Enviados, Eliminados, Spam) al hacer clic en una empresa del sidebar.
- [x] **Tema Spark Dark Mode:** Transformación visual completa al estilo Spark (Antracita/Azul Spark) con legibilidad optimizada en hilos.
- [x] **Perfil de Usuario Apple Style:** Nueva tarjeta de perfil interactiva con avatar dinámico y confirmación de cierre de sesión segura.
- [x] **UI Inspector:** Contraste mejorado manteniendo el modo claro para la lectura de correos dentro de la interfaz oscura.

## 🚀 Próximos Pasos (Instrucciones para la IA)
1. **Delegación de Tickets:** Implementar la lógica del backend para el endpoint de asignación de operadores (actualmente solo visual).
2. **Exportación:** Implementar la descarga de reportes en PDF o Excel desde el Dashboard de analíticas.
3. **Plantillas:** Sistema de respuestas rápidas (Templates) integrado en el inspector de correos.
4. **Notificaciones:** Sistema de avisos visuales (Toasts) al recibir nuevos correos.

---
**Última actualización:** lunes, 13 de abril de 2026.
**Objetivo:** Mantener el código en `index.html` como la única fuente de verdad para el panel administrativo.