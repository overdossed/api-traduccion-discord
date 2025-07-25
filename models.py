from pydantic import BaseModel
from typing import List, Optional

class Palabra(BaseModel):
    palabra: str
    traduccion: str
    categoria: str
    dificultad: str
    alternativas: Optional[List[str]] = []
    pista: Optional[str] = ""
    ejemplo: Optional[str] = ""

class NuevaPalabra(BaseModel):
    palabra: str
    traduccion: str
    categoria: str
    dificultad: str
    alternativas: Optional[List[str]] = []
    pista: Optional[str] = ""
    ejemplo: Optional[str] = "" 