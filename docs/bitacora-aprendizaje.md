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


---



## 🧭 2025-10-10 — Implementación y flujo de autenticación con Spotify

El análisis y desarrollo se centraron en construir el **flujo de autenticación** con Spotify, entendiendo cómo obtener los permisos del usuario y transformar el código de autorización en un token de acceso funcional.

Inicialmente se asumía que bastaba con una simple redirección desde el servidor Apache hacia la página de autorización de Spotify. Sin embargo, se detectó que esa redirección debía **incluir información crítica del flujo OAuth2** (como el client_id y el redirect_uri) y además **manejar el intercambio del código** devuelto por Spotify, por lo que **debía controlarse desde FastAPI**, no desde Apache.

---

Durante la implementación se estableció el flujo general:

1. **Redirección a Spotify**  
   Un método de FastAPI genera la URL de autorización con los parámetros requeridos y redirige al usuario hacia Spotify.  
   El usuario concede los permisos necesarios y Spotify redirige de vuelta al servidor con un código temporal.

2. **Recepción del código y canje por token**  
   El método `callback` recibe el código de autorización y lo envía al endpoint de Spotify para obtener el token de acceso.  
   Actualmente, solo se está manejando el **access token**, pero no el **refresh token** —esto quedó registrado como una **deuda técnica** para permitir la renovación automática de sesiones.

3. **Delegación del token al worker**  
   Una vez recibido, el token debe ser reenviado a un componente secundario (worker) que actuará como intermediario para realizar las solicitudes a Spotify.  
   Esta parte está planificada como el siguiente paso en la implementación.
---

### 🧩 Conclusión

El flujo de autenticación con Spotify **ya es funcional**, aunque con limitaciones técnicas por resolver.  
La estructura modular entre FastAPI (autenticación) y el worker (operaciones) permitirá mantener el código limpio y flexible ante futuras ampliaciones.

🧱 *Este razonamiento está directamente vinculado a la **🧭 Marco de Decisión #2 — Autenticación y manejo de tokens en Spotify***

---


## 🧭 2025-10-10 —  Flujo de autenticación en YouTube

En análisis previos se había establecido que **la autenticación dependía directamente de la API elegida**, y que por diseño debía permanecer **desacoplada de la lógica de negocio**, de modo que pudiera reemplazarse fácilmente si la API sufría alteraciones o bloqueos.

Durante esta etapa se examinó con mayor detalle el funcionamiento interno de la autenticación en la librería `ytmusicapi`, descubriendo que el proceso no emplea el flujo OAuth tradicional, sino que se basa en **encabezados (cookies)** que replican el contexto de una sesión de navegador legítima.  
A partir de esto se reconstruyó el flujo técnico real:

---

### 🔹 1. Obtención del contexto de sesión

1. El usuario inicia sesión en YouTube desde su navegador habitual.  
2. Desde esa sesión se extraen los encabezados y cookies activas (especialmente `SAPISID`, `SID` o sus equivalentes según el dominio).  
3. Con esos datos se reconstruye el **contexto de autenticación** que YouTube utiliza internamente para validar al usuario.

> En esencia, el sistema **emula una sesión de navegador ya autenticada**, evitando el flujo OAuth y aprovechando los tokens que el propio navegador mantiene válidos.

---

### 🔹 2. El problema: acceso a cookies y restricciones del navegador

Inicialmente se propuso que el **frontend actuara como puente** entre el backend y YouTube.  
La idea era que el backend enviara sus solicitudes al frontend, y este —al estar en la máquina del usuario— las reenviara directamente a YouTube usando su sesión autenticada.

Sin embargo, se descubrió un obstáculo crítico:  
los navegadores **impiden el acceso a las cookies de sesión de YouTube desde dominios externos**, bloqueando cualquier intento de obtener `SAPISID` o `SID` por políticas de seguridad (*Same-Origin Policy* y protecciones `HttpOnly`).  

Esto hacía imposible que el navegador cumpliera ese rol de intermediario directo sin vulnerar la seguridad del entorno.

---

### 🔹 3. Solución: cliente intermediario de escritorio

Para superar esta limitación se definió un **cliente intermediario local**, reutilizando el mismo programa encargado de la limpieza de metadatos.  
Este cliente tendría tres responsabilidades principales:

1. **Extraer** las cookies de sesión directamente desde el entorno local del usuario.  
2. **Recibir** las solicitudes del backend y complementarlas con los encabezados necesarios para comunicarse con YouTube.  
3. **Reenviar** las peticiones autenticadas a YouTube y **devolver** los resultados al backend.

De este modo, el flujo de autenticación se mantiene **plenamente operativo** sin violar las restricciones del navegador, y al mismo tiempo se logra una **integración natural entre el cliente local y el sistema web**.

Además, esta decisión resolvía otro requisito estructural:  
al ubicar la lógica específica de autenticación dentro del cliente, la **lógica de negocio del sistema web queda completamente desacoplada**.  
Si en el futuro se requiere cambiar de API o modificar la estrategia de autenticación, bastará con **actualizar los métodos del cliente**, sin afectar el backend ni el frontend.

---

### 🔹 4. Conclusión del flujo

Lo que comenzó como una limitación técnica —la imposibilidad del frontend de manipular cookies seguras— terminó fortaleciendo la arquitectura general.  
La autenticación de YouTube se consolidó dentro del cliente de escritorio, otorgándole un **rol central y estructural** dentro del ecosistema del proyecto.

> En resumen, el cliente no solo limpia metadatos: ahora también **funciona como puente de autenticación y ejecución segura** para las operaciones de YouTube, manteniendo el backend y el frontend libres de responsabilidades sensibles.

---
## 🧭 2025-10-28 —  Planificacion de la BD 

**Estado actual:** flujo funcional y justificado estructuralmente.  
**Pendiente:** definir y documentar la **interfaz de comunicación** entre el cliente local y el backend, garantizando un manejo encapsulado y seguro de los tokens de sesión.


###🔹 1. Planteamiento inicial: rol de la base de datos

El problema que dio origen a este análisis fue la carga masiva de datos en el frontend.
El navegador no podía manejar simultáneamente cientos de canciones sin saturarse, por lo que se concluyó que debía implementarse un sistema de carga por lotes.
Esto derivó en una cadena lógica:

El frontend solicita lotes de datos según el desplazamiento del usuario (scroll).

El backend responde a esas solicitudes recuperando fragmentos específicos desde la DB.

Para evitar sobrecargar al worker, el backend requería acceso directo a la base de datos en calidad de observador, mientras que el worker sería el único editor autorizado (agregar, modificar o eliminar registros).

El modelo final posicionó a los cuatro servicios (frontend, backend, worker e IA) como microservicios independientes, comunicados mediante HTTP, y contenedorizados para mantener su aislamiento operativo.

###🔹 2. Evaluación de tecnologías: SQL vs Redis

En un principio se asumió un enfoque clásico con SQL.
Sin embargo, al analizar los requisitos del sistema se concluyó que este modelo era ineficiente:

Se necesitaba acceso extremadamente rápido en memoria.

La base de datos debía ser dinámica y efímera (los datos se eliminan al finalizar el proceso).

La estructura de los datos ya existía en forma de diccionarios Python, lo que hacía natural un modelo key–value.

Bajo estos criterios, Redis emergió como la opción más coherente.
Además, se comprendió que Redis opera prácticamente como un espacio compartido de memoria RAM entre servicios, optimizado para accesos concurrentes.

###🔹 3. Primer diseño estructural

El esquema inicial propuso una organización independiente por fuente:
```python
YTplaylist = {id1: {...}, id2: {...}}
SPplaylist = {id1: {...}, id2: {...}}
LCplaylist = {id1: {...}, id2: {...}}
relations = {YT1: {SPid3, LCid4}, YT3: {LCid5, SPid6}}
```

Luego surgió una mejora:
a medida que el sistema detectara relaciones entre canciones de distintas fuentes, estas serían extraídas de las playlists originales y trasladadas a versiones sorted, dejando a las listas principales cada vez más ligeras y evitando duplicaciones.
Se mantendrían copias de respaldo (imagen) para recuperación ante errores.

Este modelo resultó en nueve estructuras activas: tres originales, tres sorted y tres de respaldo, más el arreglo general de relaciones.

###🔹 4. Riesgo identificado: atomización de estructuras

Durante el montaje mínimo de Redis se exploró la forma de persistir estas estructuras.
Inicialmente se pensó en almacenar una playlist completa como un único valor de texto (string).
Sin embargo, se detectó un riesgo grave: cualquier corrupción o error sobre ese string afectaría toda la playlist, y las operaciones parciales implicarían reconvertir un bloque completo de cientos de registros.

La solución fue adoptar diccionarios anidados como valores dentro de Redis, permitiendo editar o leer cada canción individualmente sin convertir estructuras completas.
Esto redujo la complejidad y mejoró la seguridad de las operaciones.

Este hallazgo marcó el punto de inflexión: Redis no sería un simple contenedor de strings, sino una base de datos semiestructurada con acceso granular a cada entrada.

###🔹 5. Optimización de búsqueda y relaciones

El siguiente cuello detectado fue el de búsqueda de relaciones.
Buscar equivalencias desde una fuente distinta implicaba iteraciones largas sobre estructuras grandes.
Para resolverlo, se diseñó una indexación auxiliar de relaciones, que mapea directamente cada ID de canción al ID de relación correspondiente:

```python
relations = {
  "rel_001": {"equivalents":
    {"yt": "yt123",
    "sp": "sp456"}}
}
relation_index = {
  "yt123": "rel_001",
  "sp456": "rel_001"}
```

Esta decisión duplicó parcialmente la información, pero redujo las búsquedas a dos consultas directas en lugar de una iteración masiva, mejorando drásticamente la velocidad.

###🔹 6. Estandarización y métodos básicos

Se unificaron todas las fuentes dentro de una sola estructura jerárquica:

```python
playlists = {
    "yt": {...},
    "sp": {...},
    "local": {...}
}
```

Con esta estructura se desarrollaron métodos básicos para:

Añadir canciones.

Obtener canciones por ID.

Crear relaciones entre canciones.

Definir búsquedas flexibles (para IA o backend).

Se acordó diferir la construcción definitiva del formato JSON de búsqueda hasta disponer de datos reales provenientes del worker.

###🔹 7. Consideraciones sobre indexación y consumo de memoria

Redis permite consultas avanzadas mediante etiquetas si los metadatos están almacenados como pares clave:valor simples.
Esto llevó a considerar una posible duplicación adicional de datos, lo que en teoría aumentaría el consumo de RAM.
Sin embargo, una estimación preliminar —90000 canciones con 15 metadatos cada una— arrojó un consumo aproximado de 500 MB, considerado aceptable.

De esta conclusión emergió un principio general de diseño:

Es preferible evitar bucles de búsqueda incluso si eso implica mayor consumo de memoria temporal.

###🔹 8. Rol del servicio de IA

Durante la simulación del comportamiento del asistente se estableció que la IA requerirá:

Un entorno Redis local para manipular sus propios filtros.

Comandos de limpieza y reconstrucción para gestionar sus estructuras auxiliares.

Capacidad para ejecutar operaciones de filtrado y conteo, a partir de las cuales inferirá resultados o heurísticas.

Se determinó que librerías como Redisearch podrían incorporarse más adelante, aunque las operaciones booleanas nativas de Redis ya ofrecen la flexibilidad necesaria.

###🔹 9. Estado actual

El sistema de almacenamiento temporal ha sido conceptualizado y estructurado con base en Redis.
Las estructuras principales y los métodos de manipulación ya están definidos en código y listos para pruebas unitarias.
Las decisiones de diseño tomadas priorizan acceso directo, modularidad y resiliencia frente a errores.

Pendiente: validar empíricamente el consumo de memoria real durante operaciones del worker y definir el formato JSON final para las consultas de la IA y el backend.

---

## 🧭 2025-11-27 — Desarrollo del módulo de captura de headers y establecimiento del puente YouTube → Worker

El bloque surgió al analizar cómo debía operar el **puente local** entre el worker y YouTube.  
El worker no puede comunicarse directamente con YouTube porque sus peticiones carecen del contexto del navegador (headers, cookies, user-agent). Esto genera respuestas inconsistentes o bloqueos.  
Por tanto, el acceso debía delegarse al cliente local del usuario, que sí puede realizar solicitudes legítimas a YouTube.

Este razonamiento llevó a una conclusión estructural:  
**para que el puente funcione, se requiere obtener los headers reales del navegador en tiempo de ejecución.**  
Ese requisito originó todo el módulo de captura de headers.

---

## Fase 1 — Exploración de métodos de obtención de headers

La primera aproximación fue investigar si los navegadores seguían almacenando tokens o cookies de sesión en sus directorios locales.  
En sistemas actuales, los navegadores utilizan contenedores aislados y cifrados, lo que vuelve inaccesible esa información.  
Este resultado descartó cualquier intento de extracción a partir del sistema de archivos.

También se consideró pedirle al usuario que copiara los headers manualmente, pero se descartó por razones de usabilidad y fiabilidad.

---

## Fase 2 — Elección del mecanismo de captura

Sin rutas externas viables, la conclusión fue que los headers debían capturarse directamente **dentro del navegador**.  
Esto llevó a la decisión de implementar una **extensión**, capaz de escuchar peticiones reales y transmitir sus headers cuando el sistema lo requiriera.

La extensión resolvió además el problema de detectar el navegador predeterminado: el usuario instala donde usa, y ese se convierte en la fuente legítima.

---

## Fase 3 — Planteamiento del flujo inicial

El primer prototipo funcionó, pero con un orden incorrecto:  
la extensión iniciaba la captura sin que el backend lo solicitara.  
La lógica debía invertirse.

Se introdujeron dos endpoints:

- uno para solicitar headers,  
- otro para recibirlos.

Esto hizo necesario el uso del **nonce**, empleado para validar que cada captura correspondiera a una solicitud específica.

---

## Fase 4 — Necesidad de un canal persistente

Durante el diseño del flujo surgió un límite arquitectónico:  
la extensión **no puede ser contactada** directamente por el backend.

Esto obligó a introducir un canal persistente iniciado desde la extensión, con **WebSockets** como solución.  
La estructura adoptada fue:

- la extensión abre la conexión,  
- el backend confirma y mantiene la sesión,  
- los pings sostienen el enlace,  
- el backend envía el nonce cuando el worker lo necesita.

---

## Fase 5 — Seguridad y control de sesiones

Aparecieron problemas de autenticación:  
no existía garantía de que la conexión proviniera de la extensión legítima, ni un mecanismo para evitar múltiples conexiones simultáneamente.

Por ello se incorporó un **segundo token**, enviado en cada ping.  
Este token permite mantener una sesión exclusiva y validar la identidad a lo largo de la conexión.

---

## Fase 6 — Diagnóstico del error 403

Durante la primera ejecución completa del WebSocket apareció un error 403 sin explicación clara.  
No provenía de la extensión, ni del navegador, ni coincidía con un fallo típico de CORS.  
Se consideraron escenarios de incompatibilidad entre FastAPI y WebSockets, pero los síntomas no encajaban.

Para aislar el error, se construyó una versión mínima del servidor WebSocket.  
En esa prueba, el WebSocket funcionó correctamente, lo que señaló que el problema estaba dentro de la estructura del backend original.

Finalmente, se identificó la causa:  
una **clase envolvente** añadida en iteraciones previas —generada durante una sesión con la IA— alteraba el routing y bloqueaba silenciosamente la inicialización del WebSocket.

Este error expuso una dinámica particular que aparece al trabajar con herramientas capaces de generar estructuras complejas: la IA puede introducir patrones un nivel por encima del dominio que uno tiene en ese momento. Esa sutil diferencia dificulta evaluar críticamente cada pieza, porque se asume —casi de forma automática— que esa complejidad responde a una razón válida.

A esto se suma otro efecto menos evidente: cuando la toma de decisiones se vuelve colaborativa, es fácil caer en un ciclo donde cada cambio, incluso los mínimos, se consulta antes con la IA. No por inseguridad, sino porque la colaboración sostenida crea una especie de “autorización compartida” que reduce la iniciativa técnica propia sin que uno lo note.

Este caso obligó a romper esa inercia. Al detener la conversación, reducir el sistema a una versión mínima y depurarlo por cuenta propia, quedó claro que a veces es necesario perder el miedo a romper las cosas: entender cada capa, reconstruirla desde lo esencial y confrontar errores que se camuflan en el flujo asistido. Ese proceso no solo devuelve la autonomía sobre la tarea, sino que permite aprender, reforzar o incluso simplificar piezas que antes parecían molestas de depurar.

---

## Conclusión

El módulo de headers quedó definido como un sistema estable compuesto por:

- una extensión que captura headers reales,  
- un canal WebSocket iniciado por la extensión,  
- un mecanismo de nonce para validar cada operación,  
- un token persistente para autenticación continua,  
- y endpoints coordinados para solicitar y recibir los headers.

La arquitectura planeada permite que el worker solicite operaciones a YouTube mediante el puente local, utilizando sesiones reales del navegador del usuario.

este bloque de la bitacora se hace en el punto donde se logro terminar el mecanismo de headers y se esta desarrollando aun los endpoints que interactuan con youtube 

