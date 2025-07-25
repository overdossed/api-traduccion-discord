import requests
import json

API_URL = "https://api-traduccion-discord-api.up.railway.app"

def test_railway_api():
    print("🧪 Probando API desplegada en Railway...")
    print(f"🌐 URL: {API_URL}")
    
    try:
        # 1. Probar endpoint principal
        print("\n1. 🏠 Probando endpoint principal...")
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ API funcionando:")
            print(f"   Mensaje: {data['mensaje']}")
            print(f"   Versión: {data['version']}")
        else:
            print(f"❌ Error: {response.status_code}")
            return
        
        # 2. Probar palabra aleatoria
        print("\n2. 🎲 Probando palabra aleatoria...")
        response = requests.get(f"{API_URL}/palabra-random")
        if response.status_code == 200:
            palabra_data = response.json()
            print("✅ Palabra obtenida:")
            print(f"   Palabra: {palabra_data['palabra']}")
            print(f"   Categoría: {palabra_data['categoria']}")
            print(f"   Dificultad: {palabra_data['dificultad']}")
            if palabra_data.get('pista'):
                print(f"   Pista: {palabra_data['pista']}")
            
            # Usar esta palabra para probar traducción
            palabra = palabra_data["palabra"]
            print(f"\n3. 🔄 Probando traducción para '{palabra}'...")
            response = requests.get(f"{API_URL}/traducir/{palabra}")
            if response.status_code == 200:
                traduccion_data = response.json()
                print("✅ Traducción obtenida:")
                print(f"   Palabra: {traduccion_data['palabra']}")
                print(f"   Traducción: {traduccion_data['traduccion']}")
                if traduccion_data.get('alternativas'):
                    print(f"   Alternativas: {traduccion_data['alternativas']}")
                if traduccion_data.get('ejemplo'):
                    print(f"   Ejemplo: {traduccion_data['ejemplo']}")
            else:
                print(f"❌ Error en traducción: {response.status_code}")
        else:
            print(f"❌ Error obteniendo palabra: {response.status_code}")
            return
        
        # 4. Probar categoría específica
        print("\n4. 🐱 Probando categoría de animales...")
        response = requests.get(f"{API_URL}/palabra-random?categoria=animals")
        if response.status_code == 200:
            animal = response.json()
            print(f"✅ Animal obtenido: {animal['palabra']} (categoría: {animal['categoria']})")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # 5. Probar estadísticas
        print("\n5. 📊 Probando estadísticas...")
        response = requests.get(f"{API_URL}/estadisticas")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas:")
            print(f"   Total palabras: {stats['total_palabras']}")
            print(f"   Por categoría: {stats['por_categoria']}")
            print(f"   Por dificultad: {stats['por_dificultad']}")
        else:
            print(f"❌ Error: {response.status_code}")
            
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
        print("✅ Tu API está funcionando perfectamente en Railway!")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. Verifica que esté desplegada en Railway.")
    except requests.exceptions.Timeout:
        print("❌ La API tardó demasiado en responder.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_railway_api() 