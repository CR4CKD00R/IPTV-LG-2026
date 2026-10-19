# GENERAR_TV_V1.PY
# Qué hace : crea la carpeta tv/ con una copia plana de todas las listas
#              limpias, renombradas sin el sufijo _limpio, para que el
#              enlace Raw sea lo más corto posible de escribir en el TV
#              (Kodi).
#              Ejemplo: paises/pe/pe_limpio.m3u  ->  tv/pe.m3u
#              NO toca la carpeta paises/ original: solo lee de ahí y
#              escribe en tv/.
# Funciones: generar_tv() recorre las subcarpetas de paises/, copia cada
#              *_limpio.m3u con el nombre corto y verifica que cada copia
#              empiece con #EXTM3U. Usa pathlib (rutas), shutil.copy2
#              (copia conservando fecha) y sys (argumentos).
# Uso      : ejecutar desde la raíz del repo:
#              python scripts/generar_tv_v1.py
#            Opcional, con rutas propias:
#              python scripts/generar_tv_v1.py <origen> <destino>

import shutil
import sys
from pathlib import Path


def generar_tv(origen, destino):
    """Copia las listas limpias a una carpeta plana sin el sufijo _limpio."""
    origen = Path(origen)   # carpeta paises/ con una subcarpeta por país
    destino = Path(destino)  # carpeta tv/ que se va a crear
    if not origen.is_dir():
        print(f"ERROR: no existe la carpeta de origen: {origen}")
        return 0

    destino.mkdir(parents=True, exist_ok=True)  # crea la carpeta si falta

    copiados = 0
    advertencias = []
    # Busca cada *_limpio.m3u dentro de las subcarpetas (paises/pe/pe_limpio.m3u)
    for archivo in sorted(origen.glob("*/*_limpio.m3u")):
        # Quita el sufijo _limpio: pe_limpio.m3u -> pe.m3u
        nuevo_nombre = archivo.name.replace("_limpio", "")
        destino_archivo = destino / nuevo_nombre
        shutil.copy2(archivo, destino_archivo)  # copia conservando fecha
        copiados += 1
        # Verificación rápida: la copia debe empezar con #EXTM3U
        primera_linea = destino_archivo.read_text(
            encoding="utf-8", errors="ignore"
        ).splitlines()[0:1]
        if not primera_linea or not primera_linea[0].startswith("#EXTM3U"):
            advertencias.append(nuevo_nombre)

    print(f"Copiados: {copiados} archivos en {destino}/")
    if advertencias:
        print("OJO, estos no empiezan con #EXTM3U, revisarlos:")
        for nombre in advertencias:
            print(f"  - {nombre}")
    return copiados


if __name__ == "__main__":
    # Rutas por defecto: paises/ -> tv/ (desde la raíz del repo)
    origen = sys.argv[1] if len(sys.argv) > 1 else "paises"
    destino = sys.argv[2] if len(sys.argv) > 2 else "tv"
    generar_tv(origen, destino)
