# 🧭 Decisión de Diseño #2 — Creación de un Módulo de Comunicación Unificado

**Fecha de decisión:** octubre 2025  
**Estado:** En definición / Base conceptual establecida  
**Prioridad:** Alta (núcleo técnico futuro)  

---

## Contexto
Durante la planificación general del sistema surgió la necesidad de **estandarizar la forma en que los módulos se comunican** entre sí (cliente, backend, worker, IA, base de datos y servicios externos).  
Hasta ese punto, cada parte implicaba definir rutas, autenticación, cifrado y validación por separado, lo que dificultaba avanzar en paralelo.

Para evitar que cada servicio “reinvente” su propia lógica de comunicación, se propuso crear un **módulo central de envío y recepción**, capaz de manejar el tráfico de datos (principalmente JSON) de manera unificada.

---

## Decisión
Diseñar un **módulo de comunicación común**, compuesto por dos partes principales:

1. **Módulo de envío** → Responsable de preparar, cifrar y despachar datos (en formato JSON) hacia otros módulos o servicios.  
   - Ejemplo de uso: `enviar(json, destino="DB")`
2. **Módulo de recepción** → Encargado de recibir, descifrar, validar y reenviar los datos al servicio interno correspondiente.  
   - Ejemplo de uso: notificar al módulo que corresponda: *“Hey, servicio X, esto es lo que te enviaron”*.

Este módulo actuará como **intermediario estándar** entre todos los componentes, haciendo que cada uno solo deba preocuparse por *qué* enviar o recibir, y no *cómo* hacerlo.

---

## Motivación
- **Unificar la lógica de transporte de datos** entre servicios, evitando código repetido.  
- **Simplificar la seguridad interna**, centralizando cifrado y autenticación en un solo punto.  
- **Facilitar el desarrollo paralelo:** cada módulo puede avanzar usando la misma interfaz de comunicación.  
- **Aprender y controlar la capa de transporte**, entendiendo cómo viajan y se validan los datos entre procesos o contenedores.

---

## Consecuencias
- El módulo deberá ser lo bastante flexible para adaptarse a distintos contextos (ej. comunicación backend–worker vs. frontend–API).  
- Habrá que definir una **“libreta de contactos”** (un sistema de etiquetas o tuplas) que indique qué servicios pueden comunicarse entre sí.  
- Incrementa la carga conceptual inicial, pero reduce la complejidad global cuando haya varios servicios en ejecución.  
- Posible futuro: implementar una capa de cifrado o serialización común para todos los intercambios internos.
---

## Alternativas consideradas
1. **Comunicación directa entre módulos:** descartada por provocar acoplamiento y duplicación de lógica.  
2. **Uso inmediato de frameworks externos (FastAPI, gRPC, etc.):** pospuesto para una etapa posterior, cuando la teoría de base esté clara y se requiera un canal real.  
3. **Diseñar desde cero toda la capa de transporte:** descartado como punto de partida, se optó por un enfoque híbrido (aprender los fundamentos mientras se construye una versión simplificada propia).

