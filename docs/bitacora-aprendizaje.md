## 2025-10-08 — Origen del concepto de módulo de comunicación

- La idea del módulo de envío y recepción surgió como una forma de **unificar la comunicación interna entre componentes** (backend, frontend, worker, IA, base de datos), evitando tener que definir rutas y autenticación por separado en cada uno.
  
- Se planteó que cada servicio pudiera **enviar o recibir JSONs** mediante una interfaz estándar (por ejemplo, `enviar(json, destino="DB")`).
  
- Durante la reflexión inicial surgió la duda de si esto **ya existía como funcionalidad en frameworks** modernos (FastAPI, gRPC, etc.), lo que llevó a investigar si valía la pena desarrollar un sistema propio o integrar herramientas existentes.
  
- Concluido: la idea se mantiene como concepto de arquitectura, pero se **pospone su implementación completa** hasta entender con más profundidad la capa de transporte de datos.
  
- Se utilizó asistencia de IA para **evaluar la viabilidad técnica y las alternativas existentes**, manteniendo la decisión final en suspenso mientras se estudian fundamentos.

  

