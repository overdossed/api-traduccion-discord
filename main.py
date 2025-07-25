from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from database import obtener_palabra_random, obtener_traduccion, agregar_palabra, contar_palabras
from models import Palabra, NuevaPalabra

app = FastAPI(title="API de Traducción para Discord Bot", version="1.0.0")

# Permitir CORS para que tu bot pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {
        "mensaje": "API de Traducción activa",
        "version": "1.0.0",
        "endpoints": [
            "/palabra-random",
            "/traducir/{palabra}",
            "/agregar-palabra",
            "/estadisticas"
        ]
    }

@app.get("/palabra-random")
def obtener_palabra_aleatoria(categoria: str = None, dificultad: str = None):
    """
    Obtiene una palabra random
    - categoria: animals, colors, food, objects, actions
    - dificultad: easy, medium, hard
    """
    palabra = obtener_palabra_random(categoria, dificultad)
    if not palabra:
        raise HTTPException(status_code=404, detail="No se encontraron palabras")
    
    return {
        "palabra": palabra["palabra"],
        "categoria": palabra["categoria"],
        "dificultad": palabra["dificultad"],
        "pista": palabra.get("pista", "")
    }

@app.get("/traducir/{palabra}")
def traducir_palabra(palabra: str):
    """Obtiene la traducción de una palabra específica"""
    traduccion = obtener_traduccion(palabra.lower())
    if not traduccion:
        raise HTTPException(status_code=404, detail="Traducción no encontrada")
    
    return {
        "palabra": palabra,
        "traduccion": traduccion["traduccion"],
        "alternativas": traduccion.get("alternativas", []),
        "categoria": traduccion.get("categoria", ""),
        "ejemplo": traduccion.get("ejemplo", "")
    }

@app.post("/agregar-palabra")
def nueva_palabra(palabra_data: NuevaPalabra):
    """Agregar una nueva palabra a la base de datos"""
    resultado = agregar_palabra(palabra_data.dict())
    return {
        "mensaje": "Palabra agregada exitosamente",
        "palabra": resultado
    }

@app.get("/estadisticas")
def obtener_estadisticas():
    """Estadísticas de la API"""
    stats = contar_palabras()
    return {
        "total_palabras": stats["total"],
        "por_categoria": stats["categorias"],
        "por_dificultad": stats["dificultades"]
    }

@app.get("/admin/palabras")
def listar_todas_palabras():
    """Obtener todas las palabras (para administración)"""
    from database import cargar_palabras
    datos = cargar_palabras()
    return datos["palabras"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 