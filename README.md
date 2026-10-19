# IPTV - LG 2026

[![LG webOS](https://img.shields.io/badge/LG-webOS-blue)](Tutorial/TUTORIAL-KODI.md)
[![Kodi](https://img.shields.io/badge/Kodi-21-green)](Tutorial/TUTORIAL-KODI.md)
[![Pluto TV](https://img.shields.io/badge/Pluto%20TV-gratis-orange)](Tutorial/TUTORIAL-PLUTO-TV-SIN-ROOT.md)

Tutorial completo y listas M3U por país para ver IPTV en un TV LG con webOS, **sin necesidad de root**.

**Probado y funcionando en webOS 4.56.35.**

**Autor:** CRACKDOOR ([CR4CKD00R](https://github.com/CR4CKD00R)).

## Table of contents

🚀 [How to use?](#how-to-use) 📺 [Playlists](#playlists) 📖 [Tutorials](#tutorials) 🔧 [Scripts](#scripts) 🔗 [Proyectos relacionados](#proyectos-relacionados) ❓ [FAQ](#faq) ⚖ [Legal](#legal) © [License](#license)

## How to use?

Pega el enlace **Raw** de una lista en Kodi (complemento IPTV Simple Client) y pulsa Open. O instala **Pluto TV** desde la LG Content Store, sin configurar nada.

## Playlists

Dos carpetas de listas:

- `paises/` — una subcarpeta por país, con la lista limpia y su reporte de caídos:
- `paises/<codigo>/<codigo>_limpio.m3u` — lista limpia del país.
- `paises/<codigo>/<codigo>_caidos.txt` — canales caídos del país.
- `RESUMEN_TOTAL.txt` — resumen de la verificación de todos los países.
- `verificacion.log` — registro de la verificación.
- `tv/` — las mismas listas limpias, con nombres cortos y sin subcarpetas, para que el enlace Raw sea más corto de escribir en el TV.

Para Kodi usa `tv/`. Ejemplos:

- Perú: `https://raw.githubusercontent.com/CR4CKD00R/IPTV-LG-2026/main/tv/pe.m3u`
- Venezuela: `https://raw.githubusercontent.com/CR4CKD00R/IPTV-LG-2026/main/tv/ve.m3u`

Para añadir un país en Kodi, crea una configuración nueva en IPTV Simple Client con el enlace Raw de ese país. Ver el tutorial de Kodi.

## Tutorials

- 📺 [TUTORIAL-KODI.md](Tutorial/TUTORIAL-KODI.md) — Homebrew Channel + Kodi + IPTV Simple Client, paso a paso.
- 🎬 [TUTORIAL-PLUTO-TV-SIN-ROOT.md](Tutorial/TUTORIAL-PLUTO-TV-SIN-ROOT.md) — Pluto TV: países disponibles, requisitos e instalación.

## Scripts

El script `verificar_paises.py` (en `Scripts/`) busca canales y prueba cuáles funcionan, generando las listas limpias en `paises/`.

Uso: `python Scripts/verificar_paises.py`

El script `generar_tv.py` (en `Scripts/`) crea la carpeta `tv/` desde `paises/`, copiando cada lista limpia con el nombre corto.

Uso: `python Scripts/generar_tv.py`

### Actualización

El script trabaja sobre la lista que descarga en ese momento. Si el proyecto principal añade canales después, esos no aparecerán hasta volver a correr el script. Por eso el script se actualizará cada cierto tiempo según el proyecto principal:

https://github.com/iptv-org/iptv/blob/master/PLAYLISTS.md

### Regla de calidad

El script prioriza 1080p solo cuando existe un único canal en ese formato. Si existen más de uno, se utiliza 720p hacia abajo.

## Proyectos relacionados

- **iptv-org/iptv** — proyecto oficial de donde salen las listas de canales. Ver la sección Resources: https://github.com/iptv-org/iptv#resources
- **webOS Dev Manager** — app para PC que instala aplicaciones en el TV en modo desarrollador. Para Windows, descarga el archivo **.msi** desde Releases: https://github.com/webosbrew/dev-manager-desktop/releases — o usa el instalador incluido en `Software/` (`webOS.Dev.Manager_1.99.20_x64_en-US.msi`).
- **Homebrew Channel** — la tienda de apps para webOS, desde donde se instala Kodi: https://github.com/webosbrew/webos-homebrew-channel — Organización: https://github.com/webosbrew
- **PuTTY** — cliente SSH alternativo para conectarse al TV. No se usa en este proyecto (Dev Manager ya incluye lo necesario). Si la página oficial no te carga, usa el instalador incluido en `Software/` (`putty-64bit-0.85-installer.msi`): https://apps.microsoft.com/detail/xpfnzksklbp7rj?hl=es-ES&gl=PE
  https://www.chiark.greenend.org.uk/\~sgtatham/putty/latest.html
- **RootMyTV** — método para conseguir root en TVs LG con webOS. No se usa en este proyecto, que funciona sin root: https://rootmy.tv/ — https://github.com/RootMyTV/RootMyTV.github.io

## FAQ

Las respuestas a las preguntas más frecuentes están en el archivo [FAQ.md](FAQ.md).

## Legal

Este repositorio no almacena archivos de video. Solo contiene archivos M3U con enlaces a señales de video, los tutoriales de instalación y el script de búsqueda y pruebas.

Los enlaces están filtrados, actualizados y probados al 17 de octubre de 2026.

También se publican y repostean enlaces de descarga e información relacionada.

No nos hacemos responsables de ningún cargo ni consecuencia por el uso que cada persona le dé al contenido o a las herramientas. Usa listas que tengas derecho a usar.

## License

Este proyecto está bajo **licencia MIT** (ver el archivo [LICENSE](LICENSE)). El contenido original (tutoriales, script y organización) es de CRACKDOOR.

El contenido de terceros que se republica aquí (información de otros proyectos, enlaces de acceso a ellos y descargas, como las listas derivadas de iptv-org) pertenece a sus respectivos autores y conserva sus propias licencias y condiciones.
