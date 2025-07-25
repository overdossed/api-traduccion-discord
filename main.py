from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import uvicorn

from models import Palabra, NuevaPalabra
from database import (
    obtener_palabra_random, 
    obtener_traduccion, 
    agregar_palabra, 
    contar_palabras,
    listar_todas_las_palabras
)

app = FastAPI(
    title="API de Traducción Discord",
    description="API para palabras y traducciones del bot de Discord",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "API de Traducción Discord v2.0",
        "endpoints": {
            "normales": "/palabra-normal - Solo palabras cotidianas",
            "warframe": "/palabra-warframe - Solo mods de Warframe", 
            "mixtas": "/palabra-mixta - Todas las palabras mezcladas",
            "traducir": "/traducir/{palabra} - Obtener traducción",
            "agregar": "/agregar-palabra - Agregar nueva palabra",
            "estadisticas": "/estadisticas - Ver estadísticas",
            "admin": "/admin/palabras - Ver todas las palabras"
        },
        "nueva_funcionalidad": "Archivos JSON separados para mejor organización"
    }

# ======================== ENDPOINTS PRINCIPALES ========================

@app.get("/palabra-normal", response_model=Palabra)
async def obtener_palabra_normal(
    categoria: Optional[str] = Query(None, description="animals, food, colors, objects, actions, concepts"),
    dificultad: Optional[str] = Query(None, description="easy, medium, hard")
):
    """Obtiene una palabra aleatoria de categorías normales (cotidianas)"""
    palabra = obtener_palabra_random(tipo="normal", categoria=categoria, dificultad=dificultad)
    
    if not palabra:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron palabras normales con los filtros especificados"
        )
    
    return palabra

@app.get("/palabra-warframe", response_model=Palabra)
async def obtener_palabra_warframe(
    dificultad: Optional[str] = Query(None, description="easy, medium, hard")
):
    """Obtiene un mod aleatorio de Warframe"""
    palabra = obtener_palabra_random(tipo="warframe", categoria="warframe_mods", dificultad=dificultad)
    
    if not palabra:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron mods de Warframe con la dificultad especificada"
        )
    
    return palabra

@app.get("/palabra-mixta", response_model=Palabra)
async def obtener_palabra_mixta(
    categoria: Optional[str] = Query(None, description="animals, food, colors, objects, actions, concepts, warframe_mods"),
    dificultad: Optional[str] = Query(None, description="easy, medium, hard")
):
    """Obtiene una palabra aleatoria de todas las categorías mezcladas"""
    palabra = obtener_palabra_random(tipo="mixto", categoria=categoria, dificultad=dificultad)
    
    if not palabra:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron palabras con los filtros especificados"
        )
    
    return palabra

# ======================== ENDPOINTS LEGACY (COMPATIBILIDAD) ========================

@app.get("/palabra-random", response_model=Palabra)
async def obtener_palabra_random_legacy(
    categoria: Optional[str] = Query(None, description="animals, food, colors, objects, actions, concepts, warframe_mods"),
    dificultad: Optional[str] = Query(None, description="easy, medium, hard"),
    tipo: Optional[str] = Query("mixto", description="normal, warframe, mixto")
):
    """Endpoint legacy para compatibilidad hacia atrás"""
    palabra = obtener_palabra_random(tipo=tipo, categoria=categoria, dificultad=dificultad)
    
    if not palabra:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron palabras con los filtros especificados"
        )
    
    return palabra

# ======================== OTROS ENDPOINTS ========================

@app.get("/traducir/{palabra}")
async def traducir_palabra(
    palabra: str,
    tipo: Optional[str] = Query("mixto", description="normal, warframe, mixto")
):
    """Obtiene la traducción de una palabra específica"""
    traduccion = obtener_traduccion(palabra, tipo=tipo)
    
    if not traduccion:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró la palabra '{palabra}' en la base de datos"
        )
    
    return traduccion

@app.post("/agregar-palabra")
async def agregar_nueva_palabra(palabra: NuevaPalabra):
    """Agrega una nueva palabra a la base de datos"""
    
    # Determinar el tipo según la categoría
    tipo = "warframe" if palabra.categoria == "warframe_mods" else "normal"
    
    palabra_dict = palabra.dict()
    
    # Agregar a la base de datos
    resultado = agregar_palabra(palabra_dict, tipo=tipo)
    
    if not resultado:
        raise HTTPException(
            status_code=400, 
            detail="La palabra ya existe o hubo un error al agregarla"
        )
    
    return {
        "message": f"Palabra '{palabra.palabra}' agregada exitosamente al archivo de palabras {tipo}",
        "palabra": palabra_dict,
        "archivo": f"palabras_{tipo}.json" if tipo != "normal" else "palabras_normales.json"
    }

@app.get("/estadisticas")
async def obtener_estadisticas(
    tipo: Optional[str] = Query("mixto", description="normal, warframe, mixto")
):
    """Obtiene estadísticas de las palabras por tipo"""
    stats = contar_palabras(tipo=tipo)
    
    return {
        "tipo": tipo,
        "estadisticas": stats,
        "archivos": {
            "normal": "palabras_normales.json",
            "warframe": "palabras_warframe.json", 
            "mixto": "Combinación de ambos archivos"
        }
    }

@app.get("/admin/palabras")
async def obtener_todas_las_palabras():
    """Endpoint administrativo - Lista todas las palabras organizadas por tipo"""
    todas = listar_todas_las_palabras()
    
    # Estadísticas rápidas
    stats = {
        "normales": len(todas["normales"]),
        "warframe": len(todas["warframe"]),
        "total_mixtas": len(todas["mixtas"])
    }
    
    return {
        "estadisticas": stats,
        "palabras": todas
    }

# ======================== ENDPOINTS DE PRUEBA ========================

@app.get("/test/categorias")
async def listar_categorias():
    """Lista todas las categorías disponibles"""
    todas = listar_todas_las_palabras()
    
    categorias_normales = set()
    categorias_warframe = set()
    
    for palabra in todas["normales"]:
        categorias_normales.add(palabra.get("categoria", "sin_categoria"))
    
    for palabra in todas["warframe"]:
        categorias_warframe.add(palabra.get("categoria", "sin_categoria"))
    
    return {
        "categorias_normales": sorted(list(categorias_normales)),
        "categorias_warframe": sorted(list(categorias_warframe)),
        "todas_las_categorias": sorted(list(categorias_normales.union(categorias_warframe)))
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 