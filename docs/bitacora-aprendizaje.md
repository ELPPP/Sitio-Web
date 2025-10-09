## 🧭 2025-10-08 — Origen del concepto de módulo de comunicación

- La idea del módulo de envío y recepción surgió como una forma de **unificar la comunicación interna entre componentes** (backend, frontend, worker, IA, base de datos), evitando tener que definir rutas y autenticación por separado en cada uno.
  
- Se planteó que cada servicio pudiera **enviar o recibir JSONs** mediante una interfaz estándar (por ejemplo, `enviar(json, destino="DB")`).
  
- Durante la reflexión inicial surgió la duda de si esto **ya existía como funcionalidad en frameworks** modernos (FastAPI, gRPC, etc.), lo que llevó a investigar si valía la pena desarrollar un sistema propio o integrar herramientas existentes.
  
- Concluido: la idea se mantiene como concepto de arquitectura, pero se **pospone su implementación completa** hasta entender con más profundidad la capa de transporte de datos.
  
- Se utilizó asistencia de IA para **evaluar la viabilidad técnica y las alternativas existentes**, manteniendo la decisión final en suspenso mientras se estudian fundamentos.





## 🧭 2025-10-08 — Replanteamiento del módulo de comunicación

Durante el diseño inicial del sistema se había considerado crear un **módulo de transporte propio**, responsable de manejar el envío y recepción de datos entre los distintos servicios (backend, worker, IA, etc.).  
La idea era contar con un bloque dedicado a la **negociación, cifrado y transferencia** de mensajes entre módulos, de forma similar a un gestor de red centralizado.

Sin embargo, una duda que quedaba por resolver era la **cantidad de tipos de peticiones** que se realizarían entre servicios.  
Esta se despejó al volver a analizar el funcionamiento de una consulta HTTP: por lo general, **no son los diseñadores quienes se adaptan a la consulta HTTP**, sino que **la consulta HTTP se adapta al tipo de datos que el servicio necesite enviar o recibir**.  
Por lo tanto, imponer un módulo rígido de comunicación significaba perder esa flexibilidad inherente.

Esto me hizo recordar que en el diseño del cliente ya había implementado una **búsqueda web segura** usando librerías como `requests`, con autenticación y manejo de tokens, lo que cumplía exactamente con el rol que yo esperaba para el módulo de envío.  
A su vez, recordé los **CTF’s** en los que había trabajado, donde se empleaban **servidores HTTP en escucha** para recibir y responder peticiones, lo que coincidía con la idea de mi módulo de recepción.

Más adelante, al profundizar en el funcionamiento real de **FastAPI** y **requests**, comprendí por qué los desarrolladores **no suelen preocuparse explícitamente por esta capa**:  
su funcionalidad ya está resuelta dentro de los frameworks modernos, que gestionan internamente la creación de endpoints, el cifrado HTTPS, la autenticación y la validación de datos.

---

### 🧩 Conclusión

El sistema ahora debe pensarse como una **colección de servicios que exponen y consumen endpoints**, en lugar de bloques que dependen de un intermediario común.  
Con esto resuelto, el siguiente paso es **planificar la arquitectura general**, definiendo cómo se comunican los servicios y qué información intercambian.

🧱 *Este razonamiento llevó directamente a la **Decisión de Diseño #3.***
