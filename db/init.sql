# Database initialization script
-- 1. USUARIOS
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE NOT NULL, -- Identificador único de Google 
    name VARCHAR(255),                      -- Para que el agente diga "Hola [Name]" 
    session_id VARCHAR(255),                -- Identificador de sesión activa para el Worker 
);

-- 2. EVENTOS
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE, -- Referencia a usuario 
    calendar_event_id VARCHAR(255),         -- ID de Google Calendar 
    name VARCHAR(255) NOT NULL,             -- Nombre del evento 
    start TIMESTAMP NOT NULL,      -- Hora inicio en UTC
    end TIMESTAMP NOT NULL,        -- Hora fin en UTC
    category VARCHAR(50)                    -- WORK, MEETING, PERSONAL, LEARNING, WELLNESS 
);

-- 3. MÉTRICAS
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE, -- Referencia a evento 
    -- Datos Duros
    completion_status VARCHAR(20) NOT NULL, -- COMPLETED, MISSED, RESCHEDULED 
    actual_duration_minutes INTEGER,        -- Duración real en minutos
    -- User Feedback (Cualitativo convertido a Cuantitativo)
    productivity_score INTEGER,             -- 1-5
    mood_score INTEGER,                     -- 1-5 
    user_comment TEXT,                      -- Lo que dijo el usuario textualmente
);