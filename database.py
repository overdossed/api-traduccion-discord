import json
import random
from typing import Optional, Dict, List

def cargar_palabras():
    """Cargar datos desde archivo JSON"""
    try:
        with open('palabras.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"palabras": []}

def guardar_palabras(datos):
    """Guardar datos al archivo JSON"""
    with open('palabras.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def obtener_palabra_random(categoria: Optional[str] = None, dificultad: Optional[str] = None):
    """Obtener una palabra aleatoria con filtros opcionales"""
    datos = cargar_palabras()
    palabras = datos["palabras"]
    
    # Filtrar por categoría y dificultad
    if categoria:
        palabras = [p for p in palabras if p["categoria"] == categoria]
    if dificultad:
        palabras = [p for p in palabras if p["dificultad"] == dificultad]
    
    if not palabras:
        return None
    
    return random.choice(palabras)

def obtener_traduccion(palabra: str):
    """Obtener la traducción de una palabra específica"""
    datos = cargar_palabras()
    for p in datos["palabras"]:
        if p["palabra"].lower() == palabra.lower():
            return p
    return None

def agregar_palabra(nueva_palabra: Dict):
    """Agregar una nueva palabra a la base de datos"""
    datos = cargar_palabras()
    datos["palabras"].append(nueva_palabra)
    guardar_palabras(datos)
    return nueva_palabra

def contar_palabras():
    """Obtener estadísticas de las palabras"""
    datos = cargar_palabras()
    palabras = datos["palabras"]
    
    categorias = {}
    dificultades = {}
    
    for p in palabras:
        categorias[p["categoria"]] = categorias.get(p["categoria"], 0) + 1
        dificultades[p["dificultad"]] = dificultades.get(p["dificultad"], 0) + 1
    
    return {
        "total": len(palabras),
        "categorias": categorias,
        "dificultades": dificultades
    } 