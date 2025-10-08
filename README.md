# Sitio-Web

> **Este repositorio es parte del proyecto principal [The Unknown name Music Transfer (TUMT)](https://github.com/ELPPP/The-Unknown-name-Music-Transfer-TUMT-).**

## 🌐 Descripción

Este módulo es un **sistema web** para sincronizar playlists de múltiples fuentes (locales y en línea, como Spotify y YouTube) mediante una arquitectura de microservicios desacoplados. Cada componente corre como un contenedor independiente y se comunica por red (HTTP/HTTPS).

El objetivo es permitir comparar, transferir y mantener la consistencia de listas de reproducción entre diferentes plataformas, empleando lógica avanzada y herramientas inteligentes.

## 🏗️ Estructura y roles de los módulos

- **frontend/**  
  Interfaz web del usuario. Permite visualizar, gestionar y transferir playlists entre plataformas. Presenta el estado del proceso y los resultados de la sincronización.

- **backend/**  
  Encargado de gestionar la comunicación con APIs externas (Spotify, YouTube, etc.) y coordinar la interacción entre el frontend y el resto de los servicios.

- **worker/**  
  Núcleo lógico del sistema. Realiza las comparaciones, análisis y procesamiento de metadatos y listas. Toda la lógica de negocio y reglas de comparación residen aquí.

- **db/**  
  Base de datos temporal. Almacena información de música local, metadatos encontrados y equivalencias entre playlists. Funciona como una “mesa de trabajo” durante el proceso y se vacía al finalizar para evitar acumulación de datos innecesarios.

- **ia/** (futuro)  
  Módulo que alojará la inteligencia artificial para análisis avanzado de metadatos y recomendaciones. Se espera que interactúe con el worker, backend y la base de datos. La arquitectura está abierta a que sea un microservicio propio o una integración con herramientas como n8n.

- **docker-compose.yml**  
  Orquestador para levantar y conectar todos los servicios en ambiente de desarrollo o despliegue.

## 🚦 Estado actual

- Estructura de carpetas definida, sin lógica implementada.
- Desarrollo en pausa mientras se exploran tecnologías y se toman decisiones de diseño.
- Las decisiones, bitácoras y experimentos se documentan en la carpeta `/docs`.

## 📚 Documentación y decisiones de diseño

Las decisiones de arquitectura, bitácoras y roadmap se encuentran en la carpeta [`/docs`](./docs/):

- [Decisiones de diseño](./docs/decisiones-de-diseno.md) (en progreso)
- [Bitácora de aprendizaje](./docs/bitacora-aprendizaje.md) (en progreso)
- [Roadmap](./docs/roadmap.md) (en progreso)

## 🤝 Colabora o acredita

Este proyecto está bajo licencia MIT.  
**Si este proyecto te inspira, ayuda o utilizas parte de su código, por favor menciona a [ELPPP](https://github.com/ELPPP) y enlaza este repositorio.**  
¡Se agradecen ideas, sugerencias y ayuda en cualquier etapa del desarrollo!

---

## 🔗 Proyecto principal y módulos relacionados

- [The Unknown name Music Transfer (TUMT)](https://github.com/ELPPP/The-Unknown-name-Music-Transfer-TUMT-) — Presentación y coordinación general.
- [Organizador de Etiquetas de Canción (módulo de escritorio)](https://github.com/ELPPP/organizador-de-etiquetas-de-cancion-) — Herramienta para limpieza y organización de metadatos musicales locales.

---

## 📄 Licencia

[MIT](LICENSE)
