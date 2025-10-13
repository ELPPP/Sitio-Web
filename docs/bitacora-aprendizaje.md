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


## 🧭 2025-10-13 — Evaluación de autenticación y elección de API para YouTube

El análisis comenzó intentando definir el **sistema de autenticación** con YouTube: cómo obtener permisos del usuario, gestionar tokens y permitir que el sistema acceda a las playlists.  
Inicialmente se asumía que el proceso sería estándar (flujo OAuth2 con redirección y almacenamiento de tokens).  
Sin embargo, rápidamente se detectó que **la forma de autenticarse depende por completo de la API utilizada** —es decir, la autenticación no es un problema independiente, sino una consecuencia de la API elegida.

Esto cambió la dirección del análisis: antes de decidir cómo autenticar, era necesario definir **qué API** se va a usar.  
A partir de ahí, el foco del razonamiento pasó de “cómo autenticamos” a “con quién autenticamos”.

---

Durante la exploración surgieron tres caminos técnicos:

1. **API oficial (YouTube Data API v3)**  
   Se comprobó que ofrece toda la información necesaria con gran precisión y estabilidad.  
   El problema está en sus **cuotas diarias extremadamente limitadas**, que restringen el número de operaciones por usuario.  
   Esto vuelve inviable el flujo principal del proyecto —migrar o sincronizar playlists grandes—, ya que podría agotarse la cuota tras unas pocas acciones.

2. **APIs no oficiales**  
   Estas librerías replican las funciones básicas de la API oficial sin límites de cuota y con autenticaciones más simples (cookies o tokens directos).  
   Aunque resuelven el cuello de botella técnico, presentan **riesgos de mantenimiento**: pueden romperse con cambios en YouTube o sufrir bloqueos eventuales.

3. **Enfoque híbrido**  
   Se propuso usar la API oficial para tareas de bajo consumo (por ejemplo, búsquedas o validaciones) y una API no oficial para operaciones pesadas (creación o lectura masiva).  
   Este equilibrio podría funcionar, pero **aumenta la complejidad estructural** y la cantidad de puntos de falla.

---

Al revisar los casos de uso, se identificaron tres flujos principales:

- **Usuarios con música local** que quieren replicar sus playlists en plataformas.  
- **Usuarios que migran playlists entre plataformas.**  
- **Usuarios que comparan o sincronizan playlists equivalentes** entre distintas fuentes (por ejemplo, entre YouTube y una carpeta local).

De los tres, si los primeros dos se hacen en volummenes muy altos de canciones (de 50 a 100)  implicarian un **mayor consumo de peticiones** y es donde las limitaciones de la API oficial se vuelven críticas.

---

El razonamiento llevó a una conclusión importante:  
el sistema de autenticación no es un problema aislado, sino **una consecuencia directa de la API seleccionada**.  
La API oficial cumple con todas las funciones, pero **no con el volumen de trabajo necesario**; por tanto, usarla sería como dejar el sistema “funcional pero débil”.  
Por otro lado, depender completamente de una API no oficial implicaría riesgos de estabilidad a largo plazo.

De ahí surgió la idea de diseñar una **capa de traducción modular** entre el sistema y las APIs, de modo que el código principal no dependa directamente de una implementación específica.  
Esto permitirá cambiar o combinar APIs sin afectar el resto del sistema, reduciendo los costos futuros de mantenimiento o portabilidad.

---

### 🧩 Conclusión

La elección definitiva de la API **queda abierta**, pero con una dirección clara:  
- El sistema debe diseñarse de forma que **pueda cambiar de API con el menor impacto posible**.  
- La autenticación se implementará **según el flujo que exija la API finalmente seleccionada**.  
- Por ahora, se asume que **la API oficial no es viable como único canal** debido a sus restricciones de cuota, y se mantendrá abierta la opción de APIs no oficiales o híbridas.

🧱 *Este razonamiento está directamente vinculado a la ** 🧭 Marco de Decisión #1 — Integración con YouTube (autenticación y capa API)**

