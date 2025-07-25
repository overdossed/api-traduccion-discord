import json
import random
from typing import Optional, Dict, Any, List
import os

def cargar_palabras(archivo: str = "palabras.json") -> Dict[str, Any]:
    """Carga palabras desde un archivo JSON específico"""
    try:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"palabras": []}
    except Exception as e:
        print(f"Error cargando {archivo}: {e}")
        return {"palabras": []}

def cargar_palabras_normales() -> Dict[str, Any]:
    """Carga solo palabras normales"""
    return cargar_palabras("palabras_normales.json")

def cargar_palabras_warframe() -> Dict[str, Any]:
    """Carga solo palabras de Warframe"""
    return cargar_palabras("palabras_warframe.json")

def cargar_palabras_mixtas() -> Dict[str, Any]:
    """Carga todas las palabras combinadas"""
    normales = cargar_palabras_normales()
    warframe = cargar_palabras_warframe()
    
    # Combinar las listas
    todas_palabras = normales["palabras"] + warframe["palabras"]
    
    return {"palabras": todas_palabras}

def guardar_palabras(datos: Dict[str, Any], archivo: str = "palabras.json") -> bool:
    """Guarda palabras en un archivo JSON específico"""
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando {archivo}: {e}")
        return False

def obtener_palabra_random(tipo: str = "mixto", categoria: Optional[str] = None, dificultad: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Obtiene una palabra aleatoria según el tipo especificado
    
    Args:
        tipo: "normal", "warframe", "mixto"
        categoria: Filtrar por categoría específica
        dificultad: Filtrar por dificultad específica
    """
    # Cargar según el tipo
    if tipo == "normal":
        datos = cargar_palabras_normales()
    elif tipo == "warframe":
        datos = cargar_palabras_warframe()
    else:  # mixto
        datos = cargar_palabras_mixtas()
    
    palabras = datos.get("palabras", [])
    
    if not palabras:
        return None
    
    # Filtrar por categoría si se especifica
    if categoria:
        palabras = [p for p in palabras if p.get("categoria") == categoria]
    
    # Filtrar por dificultad si se especifica
    if dificultad:
        palabras = [p for p in palabras if p.get("dificultad") == dificultad]
    
    # Seleccionar palabra aleatoria
    if palabras:
        return random.choice(palabras)
    
    return None

def obtener_traduccion(palabra: str, tipo: str = "mixto") -> Optional[Dict[str, Any]]:
    """
    Busca la traducción de una palabra específica
    
    Args:
        palabra: La palabra a buscar
        tipo: "normal", "warframe", "mixto"
    """
    # Cargar según el tipo
    if tipo == "normal":
        datos = cargar_palabras_normales()
    elif tipo == "warframe":
        datos = cargar_palabras_warframe()
    else:  # mixto
        datos = cargar_palabras_mixtas()
    
    palabras = datos.get("palabras", [])
    
    # Buscar la palabra (case insensitive)
    for p in palabras:
        if p.get("palabra", "").lower() == palabra.lower():
            return p
    
    return None

def agregar_palabra(nueva_palabra: Dict[str, Any], tipo: str = "normal") -> bool:
    """
    Agrega una nueva palabra al archivo correspondiente
    
    Args:
        nueva_palabra: Diccionario con los datos de la palabra
        tipo: "normal" o "warframe" - determina a qué archivo agregar
    """
    try:
        # Determinar archivo según el tipo
        if tipo == "warframe":
            archivo = "palabras_warframe.json"
            datos = cargar_palabras_warframe()
        else:
            archivo = "palabras_normales.json"  
            datos = cargar_palabras_normales()
        
        # Verificar si la palabra ya existe
        palabra_existente = any(
            p.get("palabra", "").lower() == nueva_palabra.get("palabra", "").lower()
            for p in datos.get("palabras", [])
        )
        
        if palabra_existente:
            return False
        
        # Agregar la nueva palabra
        datos["palabras"].append(nueva_palabra)
        
        # Guardar el archivo
        return guardar_palabras(datos, archivo)
        
    except Exception as e:
        print(f"Error agregando palabra: {e}")
        return False

def contar_palabras(tipo: str = "mixto") -> Dict[str, int]:
    """
    Cuenta las palabras por tipo y categoría
    
    Args:
        tipo: "normal", "warframe", "mixto"
    """
    # Cargar según el tipo
    if tipo == "normal":
        datos = cargar_palabras_normales()
    elif tipo == "warframe":
        datos = cargar_palabras_warframe()
    else:  # mixto
        datos = cargar_palabras_mixtas()
    
    palabras = datos.get("palabras", [])
    
    # Contar total
    total = len(palabras)
    
    # Contar por categoría
    categorias = {}
    for palabra in palabras:
        categoria = palabra.get("categoria", "sin_categoria")
        categorias[categoria] = categorias.get(categoria, 0) + 1
    
    # Contar por dificultad
    dificultades = {}
    for palabra in palabras:
        dificultad = palabra.get("dificultad", "sin_dificultad")
        dificultades[dificultad] = dificultades.get(dificultad, 0) + 1
    
    return {
        "total": total,
        "por_categoria": categorias,
        "por_dificultad": dificultades
    }

def listar_todas_las_palabras() -> Dict[str, List[Dict[str, Any]]]:
    """
    Lista todas las palabras organizadas por tipo
    """
    return {
        "normales": cargar_palabras_normales().get("palabras", []),
        "warframe": cargar_palabras_warframe().get("palabras", []),
        "mixtas": cargar_palabras_mixtas().get("palabras", [])
    } 