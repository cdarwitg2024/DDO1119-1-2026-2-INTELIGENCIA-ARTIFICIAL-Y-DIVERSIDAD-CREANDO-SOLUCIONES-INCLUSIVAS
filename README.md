# DDO1119-1-2026-2-INTELIGENCIA-ARTIFICIAL-Y-DIVERSIDAD-CREANDO-SOLUCIONES-INCLUSIVAS

# AgroBot - Asistente Agrícola para Discord

Bot de Discord con IA especializado en agricultura, jardinería y vida rural.
Responde cuando es mencionado con `@AgroBot [tu pregunta]`.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Linux/Mac)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar `.env` (ver `.env.example`)
6. Ejecutar: `python main.py`

## Variables de entorno

DISCORD_TOKEN=...
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini


## Uso

- Menciona al bot: `@AgroBot ¿cuándo siembro tomates en Chile?`
- Comandos slash sincronizados automáticamente al iniciar.