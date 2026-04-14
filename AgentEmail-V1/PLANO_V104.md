# Plan de Mejora - Rama v1.0.4

Documento operativo para ejecutar mejoras del producto sin perder foco en estabilidad. El objetivo es completar los pendientes de `v1.0.4` con entregables medibles y orden de ejecucion claro.

**Rama activa:** `v1.0.4`  
**Estado general:** En desarrollo  
**Ultima actualizacion:** 14 de abril de 2026

---

## 1) Objetivos de la iteracion

- Consolidar el dashboard como panel de control con datos accionables.
- Mejorar la operacion diaria de tickets (filtros, busqueda, detalle).
- Fortalecer backend con trazabilidad de cambios y validaciones.
- Cerrar la iteracion con pruebas funcionales minimas repetibles.

---

## 2) Estado actual (resumen)

### Completado
- [x] Limpieza de datos de ejemplo en frontend.
- [x] KPIs dinamicos conectados a base de datos.
- [x] Gestion de estados de ticket (pendiente/asignado/cerrado).
- [x] Asignacion de tickets a operador.
- [x] Endpoint `GET /api/stats`.
- [x] Endpoint `PUT /api/hilos/update`.

### Pendiente
- [x] Graficos de actividad (hora/dia) en dashboard.
- [x] Filtros por empresa, operador y estado.
- [x] Busqueda global por remitente/asunto/contenido.
- [x] Inspector Pro: HTML, adjuntos, historial de cambios.
- [x] Logs administrativos en backend.
- [ ] Pruebas de concurrencia, persistencia y responsive.

---

## 3) Plan de ejecucion por fases

## Fase 1 - Dashboard util para operacion
**Prioridad:** Alta  
**Meta:** Permitir analisis rapido y filtrado real de tickets.

- [x] Implementar grafico de volumen por hora y por dia (Chart.js).
- [x] Agregar filtros combinables:
  - [x] Empresa.
  - [x] Operador asignado.
  - [x] Estado del ticket.
- [x] Agregar buscador global con debounce (cliente) y soporte backend si es necesario.

**Criterios de aceptacion:**
- El dashboard refleja cambios de filtros sin recargar pagina.
- El grafico no usa datos mock.
- Busqueda devuelve resultados relevantes en menos de 300 ms con dataset local actual.

## Fase 2 - Inspector y trazabilidad de tickets
**Prioridad:** Alta  
**Meta:** Mejorar la calidad de atencion y auditoria.

- [x] Renderizado seguro de correo HTML en el panel de detalle.
- [x] Visualizacion de adjuntos (nombre, tamano, enlace/accion).
- [x] Historial de ticket:
  - [x] Cambio de estado.
  - [x] Cambio de asignacion.
  - [x] Usuario/fecha de accion.

**Criterios de aceptacion:**
- El operador puede leer correctamente correos HTML complejos.
- Se muestra evidencia de adjuntos cuando existan.
- Cada cambio de estado/asignacion queda registrado y visible.

## Fase 3 - Backend robusto y observabilidad
**Prioridad:** Media  
**Meta:** Asegurar soporte tecnico y analisis de incidentes.

- [x] Estandarizar logs de acciones administrativas en backend.
- [x] Registrar al menos: endpoint, usuario, accion, resultado, timestamp.
- [x] Validar errores esperados con respuestas consistentes (400/401/500).

**Criterios de aceptacion:**
- Los logs permiten reconstruir una accion de punta a punta.
- Los endpoints nuevos mantienen formato JSON uniforme.

## Fase 4 - QA de cierre de iteracion
**Prioridad:** Alta  
**Meta:** Evitar regresiones antes de proponer merge.

- [ ] Prueba de concurrencia con multiples operadores.
- [ ] Validacion de persistencia en SQLite tras reinicio del backend.
- [ ] Verificacion responsive (desktop y viewport reducido).
- [ ] Smoke test final:
  - [ ] Login.
  - [ ] Carga de empresas.
  - [ ] Carga de hilos.
  - [ ] Cambio de estado.
  - [ ] Asignacion de ticket.

**Criterios de aceptacion:**
- No hay errores bloqueantes en consola/servidor durante flujo principal.
- Los cambios persisten correctamente en la base de datos.

---

## 4) Riesgos y mitigacion

- **Riesgo:** Degradacion de rendimiento por filtros/busqueda en cliente.  
  **Mitigacion:** Debounce, limite de resultados, indexacion SQL si aplica.

- **Riesgo:** Renderizado HTML inseguro o inconsistente.  
  **Mitigacion:** Sanitizacion controlada y fallback a texto plano.

- **Riesgo:** Dificultad para auditar cambios sin trazas estandar.  
  **Mitigacion:** Introducir estructura de logging unificada en backend.

---

## 5) Regla de trabajo para la rama

- Todo cambio se desarrolla y valida primero en `v1.0.4`.
- No se mezcla a `main` hasta aprobacion explicita.
- Cada bloque funcional cerrado debe quedar con su checklist actualizado.

---

**Nota operativa:** actualizar este archivo al cerrar cada fase o cuando cambie la prioridad del negocio.
