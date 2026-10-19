# FAQ

## ¿Necesito root en el TV?

No. Homebrew Channel, Kodi y Pluto TV funcionan sin root. Sin root no funcionan el servicio de ejecución root, desactivar telemetría, scripts de arranque, SSH ni el modo a prueba de fallos, pero para ver IPTV no los necesitas.

## ¿Dónde descargo Dev Manager y PuTTY?

En la carpeta `Software/` de este repo están los instaladores: `webOS.Dev.Manager_1.99.20_x64_en-US.msi` y `putty-64bit-0.85-installer.msi`. También puedes descargarlos desde sus páginas oficiales (enlaces en el README).

## ¿Qué hago si un canal da "playback failed"?

La señal de ese canal está caída o bloqueada. No es un error de configuración. Prueba otro canal.

## ¿Puedo usar la lista global (index.m3u)?

No se recomienda. Tiene decenas de miles de canales, Kodi tarda muchísimo en cargarla y el TV se puede poner lento. Usa una lista por país.

## ¿Pluto TV está disponible en todos los países?

No. Está en 30 países de América y Europa, incluido Perú. La lista completa está en el tutorial de Pluto TV. Si tu país no está en la lista, la app no aparecerá en la tienda.

## ¿Funciona Pluto TV con VPN?

En la tienda de Homebrew hay una app, **WireGuard VPN**, pero **exige TV con root** (webOS 5.0 o superior) y tu propio servidor WireGuard en un país compatible: es solo un cliente, no un servicio VPN comercial con un clic. En un TV sin root no sirve. Además, la app no gestiona DNS, así que puede haber fuga de DNS y Pluto TV podría detectar tu ubicación real.

Sin root, la opción es poner la VPN en el router o compartirla desde la PC, aunque Pluto TV bloquea muchas IPs de VPN, así que no siempre funciona.

## ¿Qué TV necesito para Pluto TV?

Un TV LG Smart TV de 2016 en adelante (webOS 3.0 o superior) con conexión a internet. Si tu TV es anterior a 2016, la opción es un stick de streaming (Fire TV Stick o Roku).

## ¿La sesión de Developer Mode se vence?

Sí, hay que renovarla de vez en cuando. Sin root no se puede dejar permanente.
