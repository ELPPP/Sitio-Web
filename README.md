# Sitio-Web
Sistema web para sincronizar playlists locales y en línea, con servicios desacoplados (frontend, backend, worker, base de datos temporal e IA supervisora). Desplegable con Docker Compose.



Este repositorio contiene el sistema web de sincronización de playlists, diseñado como una arquitectura modular basada en contenedores.
Su propósito principal es comparar y gestionar diferencias entre una carpeta local de música y playlists en plataformas como Spotify, permitiendo identificar canciones faltantes, duplicadas o inconsistentes.

El sistema está compuesto por 5 servicios principales:

Frontend: interfaz gráfica web para el usuario.

Backend: punto de entrada de la API y orquestador de peticiones.

Worker: encargado de autenticaciones y análisis pesado (procesamiento de listas y validaciones).

Base de datos temporal: almacena resultados y datos intermedios de la sesión (no persistente).

IA: módulo supervisor que asiste en la sincronización y mantiene una interacción conversacional sobre música con el usuario.

Todo el sistema se levanta de forma integrada mediante Docker Compose, manteniendo los servicios aislados, escalables y fáciles de desplegar en cualquier entorno.
