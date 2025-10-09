# 📘 Registro de Decisiones de Diseño

---

## 🧭 Decisión de Diseño #2 — Creación de un Módulo de Comunicación Unificado

**Fecha de decisión:** octubre 2025  
**Estado:** En definición / Base conceptual establecida  
**Prioridad:** Alta (núcleo técnico futuro)  

---

### 🧩 Contexto
Durante la planificación general del sistema surgió la necesidad de **estandarizar la forma en que los módulos se comunican** entre sí (cliente, backend, worker, IA, base de datos y servicios externos).  
Hasta ese punto, cada parte implicaba definir rutas, autenticación, cifrado y validación por separado, lo que dificultaba avanzar en paralelo.

Para evitar que cada servicio “reinvente” su propia lógica de comunicación, se propuso crear un **módulo central de envío y recepción**, capaz de manejar el tráfico de datos (principalmente JSON) de manera unificada.

---

### ⚙️ Decisión
Diseñar un **módulo de comunicación común**, compuesto por dos partes principales:

1. **Módulo de envío** → Responsable de preparar, cifrar y despachar datos (en formato JSON) hacia otros módulos o servicios.  
   - Ejemplo de uso: `enviar(json, destino="DB")`

2. **Módulo de recepción** → Encargado de recibir, descifrar, validar y reenviar los datos al servicio interno correspondiente.  
   - Ejemplo de uso: notificar al módulo que corresponda: *“Hey, servicio X, esto es lo que te enviaron”*.

Este módulo actuará como **intermediario estándar** entre todos los componentes, haciendo que cada uno solo deba preocuparse por *qué* enviar o recibir, y no *cómo* hacerlo.

---

### 🎯 Motivación
- **Unificar la lógica de transporte de datos** entre servicios, evitando código repetido.  
- **Simplificar la seguridad interna**, centralizando cifrado y autenticación en un solo punto.  
- **Facilitar el desarrollo paralelo:** cada módulo puede avanzar usando la misma interfaz de comunicación.  
- **Aprender y controlar la capa de transporte**, entendiendo cómo viajan y se validan los datos entre procesos o contenedores.

---

### ⚖️ Consecuencias
- El módulo deberá ser lo bastante flexible para adaptarse a distintos contextos (ej. comunicación backend–worker vs. frontend–API).  
- Habrá que definir una **“libreta de contactos”** (un sistema de etiquetas o tuplas) que indique qué servicios pueden comunicarse entre sí.  
- Incrementa la carga conceptual inicial, pero reduce la complejidad global cuando haya varios servicios en ejecución.  
- Posible futuro: implementar una capa de cifrado o serialización común para todos los intercambios internos.

---

### 🔀 Alternativas consideradas
1. **Comunicación directa entre módulos:** descartada por provocar acoplamiento y duplicación de lógica.  
2. **Uso inmediato de frameworks externos (FastAPI, gRPC, etc.):** pospuesto para una etapa posterior, cuando la teoría de base esté clara y se requiera un canal real.  
3. **Diseñar desde cero toda la capa de transporte:** descartado como punto de partida; se optó por un enfoque híbrido (aprender los fundamentos mientras se construye una versión simplificada propia).

---

## 🧭 Decisión de Diseño #3 — Replanteamiento del módulo de comunicación

**Fecha de decisión:** octubre 2025  
**Estado:** Conclusión del análisis / Cambio de enfoque  
**Prioridad:** Alta  

---

### 🧩 Contexto
Durante la planificación inicial se había propuesto construir un **módulo propio de envío y recepción** que centralizara la comunicación entre todos los servicios del sistema (backend, worker, IA, frontend, base de datos, etc.).  
La idea original era disponer de un bloque independiente capaz de gestionar **autenticación, cifrado, enrutamiento y transporte de datos**, de forma estandarizada entre componentes.

Sin embargo, el análisis posterior —registrado en la *bitácora del 2025-10-08*— permitió comprender que esta solución **replicaba capacidades que ya ofrecen los frameworks modernos**.  
La observación clave fue que las consultas HTTP/HTTPS **no requieren un diseño fijo previo**, sino que se **adaptan dinámicamente** al tipo de dato o estructura que el servicio necesite transferir.  
Por tanto, crear un módulo genérico y rígido implicaba perder flexibilidad y complejidad innecesaria.

---

### 🔍 Descubrimiento técnico
Durante la revisión de librerías y pruebas con el cliente de escritorio, se identificó que:

- La librería **`requests`** ya cumple el rol previsto para el “módulo de envío”, gestionando tokens, cifrado y peticiones HTTP seguras.  
- Frameworks como **FastAPI** implementan de forma nativa el comportamiento de un “módulo de recepción”, exponiendo endpoints que escuchan y responden peticiones bajo protocolos seguros.  

De esta manera, el conjunto **FastAPI + requests** resuelve de forma completa la capa de transporte de datos que originalmente se pensaba construir desde cero.

---

### ⚙️ Decisión
El sistema adoptará un **modelo basado en servicios que exponen y consumen endpoints HTTP**, reemplazando la idea del bloque de comunicación por un **patrón distribuido de interacción directa entre módulos**.  

Cada componente (backend, worker, IA, etc.) podrá:
- Exponer sus propios endpoints mediante FastAPI.  
- Consumir los de otros módulos mediante `requests` u otra librería equivalente.  

No se desarrollará un módulo de transporte independiente, sino que la comunicación formará parte natural de la lógica de cada servicio.

---

### ⚖️ Consecuencias técnicas
- Se reduce significativamente la complejidad de implementación y mantenimiento.  
- Se gana compatibilidad inmediata con estándares HTTP y herramientas de desarrollo modernas.  
- Las decisiones futuras de arquitectura se concentrarán en **cómo se comunican los servicios** (qué datos, cuándo y bajo qué permisos), en lugar de reinventar la capa de transporte.

📎 *Referencia:* Véase la **bitácora de 2025-10-08 — Replanteamiento del módulo de comunicación** para el razonamiento completo.

---

## 🧭 Decisión de Diseño #4 – Esquema de interacción entre servicios

**Fecha de decisión:** octubre 2025  
**Estado:** Diseño conceptual validado  
**Prioridad:** Media / Base para futuras iteraciones  

---

### 🧩 Contexto
Con la capa de transporte ya replanteada (véase Decisión de Diseño #3), se procedió a construir un **primer esquema conceptual de interacción** entre los distintos servicios del sistema.  
El objetivo fue definir el flujo general de información y responsabilidades entre el **cliente local**, el **backend**, el **worker**, la **IA** y las **APIs externas**.

<p align="center">
  <img src="../esquemas%20y%20planificaciones/diagramas%20de%20ineraccion.drawio.png" width="600" alt="Diagrama de interacción entre servicios">
</p>

### ⚙️ Descripción del diseño actual
El diagrama elaborado muestra una arquitectura **orientada a eventos y peticiones**, con diferentes fases de operación representadas por flujos de colores:

1. **Fase de autorización (blanca):**  
   - El backend gestiona la autenticación con las APIs externas (ej. Spotify, YouTube).  
   - Los tokens o credenciales resultantes se almacenan de forma segura para permitir operaciones posteriores.

2. **Fase de inicialización (azul):**  
   - El sistema obtiene las listas de reproducción disponibles y los metadatos base desde las APIs y el cliente local.  
   - Estos datos permiten al usuario definir la configuración inicial del proceso de sincronización.

3. **Fase de configuración (verde):**  
   - El usuario emite órdenes o configuraciones personalizadas (por ejemplo, reglas de sincronización o filtros).  
   - Estas órdenes se comunican al backend, que las distribuye a los servicios correspondientes.

4. **Fase de trabajo (morado):**  
   - El **worker** ejecuta las tareas solicitadas (comparación, reconstrucción de listas, obtención de canciones).  
   - Durante este bucle de trabajo, el worker puede consultar a la **IA** cuando no esté seguro sobre cómo proceder o cuando deba interpretar patrones musicales o de preferencia.  
   - El estado de progreso se actualiza continuamente hacia el backend, que lo transmite al frontend para su visualización.

5. **Fase de finalización (amarilla):**  
   - Una vez completadas las operaciones, se procede a la creación de listas equivalentes en las plataformas externas.  
   - Cada API confirma la operación y el backend consolida el resultado en la base de datos.

---

### 🧠 Rol de la IA
La IA cumple un papel doble:
- Asiste al worker en decisiones complejas o contextuales.  
- Interactúa con el usuario para analizar patrones musicales, emociones o preferencias, generando configuraciones automáticas o sugerencias personalizadas.








<!-- 
==============================  
🧩 PLANTILLA PARA NUEVAS DECISIONES DE DISEÑO  
(Este bloque no se mostrará en GitHub)
==============================  

## 🧭 Decisión de Diseño #X — [Título breve y descriptivo]

**Fecha de decisión:** [mes año]  
**Estado:** [Propuesta / Aprobada / En desarrollo / Descartada]  
**Prioridad:** [Alta / Media / Baja]  

---

### 🧩 Contexto
Explica qué problema, necesidad o duda originó esta decisión.  
Incluye el razonamiento técnico o conceptual que llevó a considerar un cambio.

---

### ⚙️ Decisión
Describe qué se decidió exactamente.  
Debe poder leerse de forma independiente (por ejemplo, “Se adopta FastAPI como módulo receptor de peticiones HTTP internas…”).

---

### 🎯 Motivación
Enumera las razones principales que justifican la decisión:  
- Beneficios esperados  
- Problemas que resuelve  
- Qué aprendizaje técnico la respalda  

---

### ⚖️ Consecuencias
Indica efectos positivos y negativos de la decisión:  
- Cambios en la arquitectura o dependencias  
- Impacto en la complejidad  
- Qué se deberá revisar o adaptar más adelante  

---

### 🔀 Alternativas consideradas
1. Alternativa 1 — razones de descarte.  
2. Alternativa 2 — razones de descarte.  
3. [Opcional] Referencias cruzadas a bitácoras o diagramas.

---

📎 *Referencia:* [Bitácora relacionada o fuente de análisis]
-->



---

### ✅ Conclusión
Este diseño refleja el primer modelo operativo funcional del sistema.  
Aunque aún es conceptual, establece las relaciones básicas y flujos de comunicación que guiarán el desarrollo modular de cada componente.

📎 *Diagrama asociado:* `diagrama de interacción entre servicios.png`
