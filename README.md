# CHECK QBITTORRENT

Script para comprobar a través de la API de qBittorrent que no hay mas torrents pausados, parados o con error de los pasados con la variable --pausado Ejemp. --pausado 2, también podemos saber cuantos torrents no están conectados al tracker, esos suelen estar así cuando sale un REPACK, etc. y se quedan los antiguos sin sedear por eliminación en el tracker pasándole la variable --no_tracker Ejemp. --no_tracker 4, si le pasamos la variable --name nos incluye el nombre del torrent, y por último si le pasamos --resumen nos envia un resumen del estado de nuestros torrents siempre que --pausado o --no_tracker hayan sido positivos.

En el caso de no especificar ninguna variable en el script los valores de --pausado y --no_tracker serán por defecto 1.

En el caso de especificar en las variables --pausado y --no_tracker un 0 esa función no se comprobará.

Si el resultado de (--pausado o --no_tracker) es positivo envia un mensaje a Telegram.

Si incluimos --resumen en el caso de que se cumpla --pausado o --no_tracker nos enviará un resumen del estado de todos los torrents a Telegram. 

Variables a configurar dentro del script check_qb.py:

  - QB_IP = 'TU_QB_IP'
  - QB_PORT = 'TU_QB_PORT'
  - QB_USER = 'TU_QB_USER'
  - QB_PASSWORD = 'TU_QB_PASSWORD'
  - TELEGRAM_BOT_TOKEN = 'TU_TELEGRAM_BOT_TOKEN'
  - TELEGRAM_CHAT_ID = 'TU_TELEGRAM_CHAT_ID'

En mi caso ejecuto el script con un cron cada día a las 7:00 h. 0 7 * * *

Ejemplo: _python3 /mnt/user/appdata/qbittorrent/scripts/check_qb.py --pausado 1 --no_tracker 1 --name --resumen_

Antes de ejecutar el script hay que instalar esta librería mediante: pip install qbittorrent-api

En el caso de Unraid a través de Nerdtools hay que activar los siguientes complementos: python-pip, python-setuptools, python3.

En el caso de Unraid a través del User Scripts hay que crear un script con lo siguiente: pip3 install qbittorrent-api y decirle "At First Array Start Only".

Resumiento le podemos pasar al script las siguientes variables:

**--pausado** = Umbral de torrents en pausa para enviar la notificación a Telegram.

**--no_tracker** = Umbral de torrents con trackers "Not working" para enviar la notificación a Telegram.

**--name** = Incluir nombre/s de torrent/s afectados en la notificación a Telegram.

**--resumen** = Incluye un resumen con el estado de todos los torrents que tenemos en QBittorrent.

Funcionando en qBittorrent v4.6.5
