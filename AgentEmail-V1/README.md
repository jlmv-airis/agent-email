# 📧 Agent Email AIRIS - Versión V1

Este es el sistema SaaS unificado de gestión de correos electrónicos. Se ha refactorizado para eliminar dependencias externas (como n8n) y utilizar una arquitectura limpia de **Python (Flask) + SQLite**.

## 📌 Estado Actual del Proyecto
- **Versión:** v1.0.6 (Control Center Pro) - **REMASTERIZADA**.
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

## ✅ Hitos Alcanzados (Versión 1.0.6)
- [x] **Dashboard Unificado:** Título de encabezado fijo y reubicación dinámica de títulos de vista para mayor claridad estructural.
- [x] **Métricas Pro Compactas:** Widgets de KPIs rediseñados en una sola línea con iconografía SVG vectorial y efectos de iluminación.
- [x] **Centro de Herramientas Avanzado:** Unificación de búsqueda global de ancho completo, filtros inteligentes y botones de acción en un solo bloque funcional.
- [x] **Filtros Temporales y Etiquetas:** Implementación de filtrado por rango de fecha (Hoy, Ayer, 7 días) y sistema inicial de categorización por etiquetas.
- [x] **Sistema de Notificaciones (Toasts):** Implementación de avisos visuales discretos y elegantes (Verde Esmeralda / Rojo) para retroalimentación de procesos en tiempo real.
- [x] **Optimización de Gráficas:** Mejora de contraste en Chart.js con textos y ejes en blanco hueso, eliminando la invisibilidad en modo oscuro.
- [x] **Precisión Temporal:** Visualización de hora destacada (blanco puro) debajo de la fecha en la lista de correos.
- [x] **Refactorización de Interfaz:** Limpieza del header superior para un aspecto más minimalista y profesional.
- [x] **Interfaz Inspector Estilo Gmail:** Implementación del rediseño visual de la ventana de visualización de correos para que se asemeje a la interfaz de Gmail, con énfasis en legibilidad y estilo moderno.

## 🚀 Próximos Pasos (V1.0.9)
1. **Sistema de Etiquetas Dinámico:** Detección automática de etiquetas (Urgente, Soporte, etc.) basada en el contenido y visualización de badges de colores.
2. **Delegación de Tickets:** Implementar la lógica del backend para el endpoint de asignación de operadores.
3. **Exportación:** Implementar la descarga de reportes en PDF o Excel desde el Dashboard.
4. **Modo Oscuro/Claro:** Garantizar consistencia absoluta en el tema visual.

---
**Última actualización:** miércoles, 15 de abril de 2026.
**Objetivo:** Mantener el código en `index.html` como la única fuente de verdad para el panel administrativo.

