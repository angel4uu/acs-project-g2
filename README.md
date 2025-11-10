# Calendar Manager Agent

## Descripción del Proyecto

Este proyecto implementa un Sistema de Agente Gestor de Calendario, una aplicación modular diseñada para la gestión inteligente de calendarios personales mediante agentes cognitivos.

El propósito principal del sistema es combinar automatización, análisis de productividad y orquestación distribuida para generar planes diarios personalizados y gestionar eventos de calendario de manera adaptativa.

## Arquitectura General

La arquitectura está compuesta por múltiples microservicios que cooperan entre sí, desplegados como contenedores Docker y orquestados mediante Docker Compose.

Los componentes principales del sistema son:

- **Agent Server (`agent_server`):**
  - Servidor principal basado en FastAPI que expone la API del agente cognitivo (ADK).
  - Gestiona la interacción con el usuario, la autenticación y la orquestación de herramientas.
- **Worker Server (`worker_server`):**
  - Servicio asíncrono que consume mensajes de RabbitMQ.
  - Responsable de ejecutar tareas programadas, recordatorios y flujos de seguimiento.
- **PostgreSQL (`postgres`):**
  - Base de datos relacional para la persistencia de datos.
  - Almacena información de usuarios, eventos y métricas de productividad.
- **RabbitMQ (`rabbitmq`):**
  - Broker de mensajería que gestiona la comunicación asíncrona entre el `Agent Server` y el `Worker Server`.

---

## Requisitos Previos

Es necesario tener instaladas las siguientes herramientas en el sistema local:

- Docker
- Docker Compose

---

## Instalación y Ejecución

Siga estos pasos para configurar e iniciar el entorno de desarrollo local.

1.  **Clonar el Repositorio**

    - Obtenga una copia local del proyecto.

2.  **Configurar el Entorno**

    - Copie el archivo `.env.example` y renómbrelo a `.env`.
    - Modifique el archivo `.env` con las credenciales y configuraciones de puertos deseadas para la base de datos, RabbitMQ y el servidor del agente.

3.  **Construir e Iniciar los Servicios**

    - Abra una terminal en el directorio raíz del proyecto y ejecute el siguiente comando:

    <!-- end list -->

    ```bash
    docker-compose up --build
    ```

    - Este comando construirá las imágenes de los contenedores (si no existen) y levantará todos los servicios definidos.

---

## Acceso al Sistema

Una vez que todos los contenedores estén en ejecución:

- **Interfaz del Agente (GUI):**
  - Acceda a la interfaz web del agente en `http://localhost:8000` (o el puerto configurado para `AGENT_PORT` en su archivo `.env`).
- **Panel de RabbitMQ:**
  - Acceda al panel de monitoreo de RabbitMQ en `http://localhost:15672` (o el puerto `RABBITMQ_UI_PORT`).
- **Base de Datos:**
  - Puede conectarse a la base de datos PostgreSQL en `localhost` a través del puerto `POSTGRES_PORT` definido.
