# =====================================================================
# ARCHIVO   : verificar_todos_paises_v3.py
# AUTOR     : CRACKDOOR (CR4CKD00R) - https://github.com/CR4CKD00R
# LICENCIA  : MIT (ver LICENSE en la raíz del proyecto)
# QUÉ HACE  : Verifica TODOS los países de iptv-org (188 países).
#             Descarga cada lista, verifica qué canales responden y
#             genera listas limpias organizadas en carpetas por país.
#             Prefiere 720p o menos, pero conserva 1080p si es la
#             única versión del canal.
#             Verifica con HEAD y, si el servidor lo rechaza, respalda
#             con GET (solo el primer byte) para evitar falsos caídos.
# FUNCIONES : descargar_lista, verificar_url, procesar_pais,
#             extraer_nombre_base, extraer_resolucion, obtener_paises
# POR QUÉ   : Las listas de iptv-org cambian con el tiempo; algunos
#             canales se caen. Este script genera listas limpias para
#             todos los países sin cargar canales muertos.
# USO       : python verificar_todos_paises_v3.py
#             Genera:
#               paises/<codigo>/<codigo>_limpio.m3u
#               paises/<codigo>/<codigo>_caidos.txt
#               RESUMEN_TOTAL.txt
# NOTA      : Tarda bastante (188 países, miles de canales).
#             Puedes dejarlo corriendo y revisar el progreso en
#             verificacion.log
# =====================================================================

import re
import urllib.request
import urllib.error
import concurrent.futures
import os
import time

# Segundos de espera por canal antes de marcarlo como caído
TIMEOUT = 8

# Códigos HTTP que se consideran "funciona"
OK_CODES = {200, 206, 301, 302, 303, 307, 308}

# Carpeta base de salida
SALIDA = "paises"


def descargar_lista(url):
    """Descarga una lista M3U y la devuelve como texto."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def verificar_url(url):
    """Verifica si una URL de stream responde. Devuelve (funciona, codigo)."""
    if url.startswith("#EXTVLCOPT"):
        return True, "VLCOPT"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    # 1) Intento con HEAD (rápido, no descarga nada)
    try:
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            if resp.status in OK_CODES:
                return True, resp.status
    except urllib.error.HTTPError as e:
        if e.code in OK_CODES:
            return True, e.code
        # HEAD rechazado (405/403/501...): puede ser un falso caído,
        # se intenta con GET antes de marcarlo como caído.
    except Exception:
        # Error de conexión o tiempo de espera: se intenta con GET.
        pass
    # 2) Respaldo con GET (solo el primer byte, para no descargar el stream)
    try:
        headers_rango = dict(headers)
        headers_rango["Range"] = "bytes=0-0"
        req = urllib.request.Request(url, method="GET", headers=headers_rango)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status in OK_CODES, resp.status
    except urllib.error.HTTPError as e:
        return e.code in OK_CODES, e.code
    except Exception:
        return False, "000"


def extraer_nombre_base(nombre_canal):
    """Quita resolución y extras para agrupar versiones del mismo canal."""
    base = re.sub(r"\s*\(\d+[pi]\)", "", nombre_canal, flags=re.IGNORECASE)
    base = re.sub(r"\s*\[[^\]]*\]", "", base)
    base = re.sub(r"\s+\b(HD|SD|FHD|UHD|4K)\b\s*$", "", base, flags=re.IGNORECASE)
    return base.strip().lower()


def extraer_resolucion(nombre_canal):
    """Extrae el número de resolución (720, 1080) o 0 si no tiene."""
    m = re.search(r"\((\d+)[pi]\)", nombre_canal, re.IGNORECASE)
    if m:
        return int(m.group(1))
    if re.search(r"\b4K\b", nombre_canal, re.IGNORECASE):
        return 2160
    return 0


def obtener_paises():
    """Obtiene la lista de códigos de país desde PLAYLISTS.md de iptv-org."""
    print("Obteniendo lista de países...")
    url = "https://raw.githubusercontent.com/iptv-org/iptv/master/PLAYLISTS.md"
    contenido = descargar_lista(url)
    # Busca patrones como countries/pe.m3u
    codigos = sorted(set(re.findall(r"countries/([a-z]{2})\.m3u", contenido)))
    print(f"Países encontrados: {len(codigos)}")
    return codigos


def procesar_pais(codigo, indice, total):
    """Procesa un país: descarga, verifica, genera limpio + reporte."""
    log = f"[{indice}/{total}] {codigo}..."
    print(log)
    with open("verificacion.log", "a", encoding="utf-8") as f:
        f.write(log + "\n")

    url = f"https://iptv-org.github.io/iptv/countries/{codigo}.m3u"
    try:
        contenido = descargar_lista(url)
    except Exception as e:
        print(f"  Error descargando {codigo}: {e}")
        return codigo, 0, 0, 0

    # Parsea canales
    lineas = contenido.split("\n")
    canales = []
    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#EXTINF"):
            partes = lineas[i].rsplit(",", 1)
            nombre_canal = partes[1].strip() if len(partes) > 1 else "Sin nombre"
            bloque = [lineas[i]]
            url_real = None
            j = i + 1
            while j < len(lineas) and not lineas[j].startswith("#EXTINF"):
                bloque.append(lineas[j])
                if lineas[j].strip().startswith("http"):
                    url_real = lineas[j].strip()
                j += 1
            if url_real:
                canales.append((bloque, url_real, nombre_canal))
            i = j
        else:
            i += 1

    total_canales = len(canales)

    # Verifica en paralelo
    resultados = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futuros = {executor.submit(verificar_url, u): u for _, u, _ in canales}
        for futuro in concurrent.futures.as_completed(futuros):
            u = futuros[futuro]
            try:
                funciona, codigo_http = futuro.result()
            except Exception:
                funciona, codigo_http = False, "000"
            resultados[u] = (funciona, codigo_http)

    # Agrupa por nombre base, elige menor resolución que funcione
    grupos = {}
    caidos = []
    for bloque, url_real, nombre_canal in canales:
        funciona, codigo_http = resultados[url_real]
        if not funciona:
            caidos.append((nombre_canal, url_real, codigo_http))
            continue
        base = extraer_nombre_base(nombre_canal)
        res = extraer_resolucion(nombre_canal)
        if base not in grupos:
            grupos[base] = []
        grupos[base].append((res, bloque))

    limpios = []
    for base, versiones in grupos.items():
        versiones.sort(key=lambda x: x[0])
        limpios.append(versiones[0][1])

    # Crea carpeta y guarda archivos
    carpeta = os.path.join(SALIDA, codigo)
    os.makedirs(carpeta, exist_ok=True)

    with open(os.path.join(carpeta, f"{codigo}_limpio.m3u"), "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for bloque in limpios:
            f.write("\n".join(bloque) + "\n")

    with open(os.path.join(carpeta, f"{codigo}_caidos.txt"), "w", encoding="utf-8") as f:
        f.write(f"Canales caídos - {codigo}\n")
        f.write(f"Total: {total_canales} | Funcionan: {len(limpios)} | Caídos: {len(caidos)}\n\n")
        for nombre_canal, url_real, codigo_http in caidos:
            f.write(f"  - {nombre_canal} | {url_real} | HTTP {codigo_http}\n")

    resultado = f"  Total: {total_canales} | Funcionan: {len(limpios)} | Caídos: {len(caidos)}"
    print(resultado)
    with open("verificacion.log", "a", encoding="utf-8") as f:
        f.write(resultado + "\n")

    return codigo, total_canales, len(limpios), len(caidos)


def main():
    print("Verificador COMPLETO de iptv-org - Todos los países")
    print("Prefiere 720p o menos, conserva 1080p si es la única versión.")
    print("=" * 60)

    paises = obtener_paises()
    total_paises = len(paises)

    resumen = []
    inicio = time.time()

    for idx, codigo in enumerate(paises, 1):
        try:
            resultado = procesar_pais(codigo, idx, total_paises)
            resumen.append(resultado)
        except Exception as e:
            print(f"Error con {codigo}: {e}")
            resumen.append((codigo, 0, 0, 0))

    # Resumen total
    total_canales = sum(r[1] for r in resumen)
    total_funcionan = sum(r[2] for r in resumen)
    total_caidos = sum(r[3] for r in resumen)
    duracion = time.time() - inicio

    with open("RESUMEN_TOTAL.txt", "w", encoding="utf-8") as f:
        f.write("RESUMEN TOTAL - Verificación iptv-org\n")
        f.write(f"Países: {total_paises}\n")
        f.write(f"Canales verificados: {total_canales}\n")
        f.write(f"Funcionan: {total_funcionan}\n")
        f.write(f"Caídos: {total_caidos}\n")
        f.write(f"Tiempo: {duracion/60:.1f} minutos\n\n")
        f.write("Por país:\n")
        for codigo, tot, func, caid in sorted(resumen):
            f.write(f"  {codigo}: Total {tot} | Funcionan {func} | Caídos {caid}\n")

    print(f"\nListo en {duracion/60:.1f} minutos.")
    print(f"Total: {total_canales} canales | Funcionan: {total_funcionan} | Caídos: {total_caidos}")
    print("Revisa RESUMEN_TOTAL.txt y las carpetas en paises/")


if __name__ == "__main__":
    main()
