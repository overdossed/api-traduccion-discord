# 🌍 API de Traducción para Discord Bot

API RESTful para obtener palabras aleatorias en inglés con sus traducciones al español, diseñada específicamente para juegos de traducción en Discord.

## 🚀 Características

- ✅ Palabras organizadas por categorías (animales, comida, colores, objetos, acciones, conceptos)
- ✅ Tres niveles de dificultad (fácil, medio, difícil)
- ✅ Traducciones con alternativas aceptadas
- ✅ Pistas y ejemplos de uso
- ✅ Estadísticas de la base de datos
- ✅ Endpoint para agregar nuevas palabras
- ✅ Documentación automática con FastAPI

## 📋 Endpoints

### `GET /`
Información general de la API

### `GET /palabra-random`
Obtiene una palabra aleatoria
- **Parámetros opcionales:**
  - `categoria`: animals, colors, food, objects, actions, concepts
  - `dificultad`: easy, medium, hard

### `GET /traducir/{palabra}`
Obtiene la traducción de una palabra específica

### `POST /agregar-palabra`
Agrega una nueva palabra a la base de datos

### `GET /estadisticas`
Estadísticas de la base de datos

### `GET /admin/palabras`
Lista todas las palabras (administración)

## 🛠️ Instalación Local

```bash
# Clonar repositorio
git clone [tu-repo]
cd mi-api-traduccion

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
uvicorn main:app --reload
```

La API estará disponible en: http://localhost:8000

## 📖 Documentación

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔧 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **JSON** - Base de datos simple

## 🌐 Despliegue

Compatible con Railway, Heroku, y otros servicios de hosting que soporten Python.

## 📊 Estructura de Datos

```json
{
  "palabra": "cat",
  "traduccion": "gato",
  "categoria": "animals",
  "dificultad": "easy",
  "alternativas": ["felino"],
  "pista": "Animal doméstico que maúlla",
  "ejemplo": "The cat is sleeping on the sofa"
}
``` 