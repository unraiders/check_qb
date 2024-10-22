# info: https://github.com/unraiders/check_qb/

import qbittorrentapi
import requests
import argparse
from datetime import datetime
import time

# Variables de configuración
QB_IP = 'TU_QB_IP'
QB_PORT = 'TU_QB_PORT'
QB_USER = 'TU_QB_USER'
QB_PASSWORD = 'TU_QB_PASSWORD'
TELEGRAM_BOT_TOKEN = 'TU_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'TU_TELEGRAM_CHAT_ID'

# Función para contar torrents en pausa
def get_paused_torrents():
    torrents = qb.torrents_info()
    paused_torrents = []
    for torrent in torrents:
        if torrent.state in ['pausedUP', 'pausedDL', 'stoppedUP', 'stoppedDL', 'error', 'unknown']:  # Ajuste para los estados de pausa, stop, error o desconocido
            paused_torrents.append(torrent)
    # Ordenar torrents por nombre
    paused_torrents.sort(key=lambda x: x.name)
    return paused_torrents

# Función para contar torrents con trackers 'Not working'
def get_not_working_trackers():
    torrents = qb.torrents_info()
    not_working_torrents = []
    for torrent in torrents:
        trackers = qb.torrents_trackers(torrent.hash)
        for tracker in trackers:
            if tracker['status'] == 4:
                not_working_torrents.append(torrent)
                break  # Contamos el torrent una vez si tiene al menos un tracker 'Not working'
    # Ordenar torrents por nombre
    not_working_torrents.sort(key=lambda x: x.name)
    return not_working_torrents

# Función para contar torrents con trackers 'Updating'
def get_updating_trackers():
    torrents = qb.torrents_info()
    updating_torrents = []
    for torrent in torrents:
        trackers = qb.torrents_trackers(torrent.hash)
        for tracker in trackers:
            if tracker['status'] == 3:
                updating_torrents.append(torrent)
                break  # Contamos el torrent una vez si tiene al menos un tracker 'Updating'
    # Ordenar torrents por nombre
    updating_torrents.sort(key=lambda x: x.name)
    return updating_torrents

# Función para contar torrents con trackers 'Working'
def get_working_trackers():
    torrents = qb.torrents_info()
    working_torrents = []
    for torrent in torrents:
        trackers = qb.torrents_trackers(torrent.hash)
        for tracker in trackers:
            if tracker['status'] == 2:
                working_torrents.append(torrent)
                break  # Contamos el torrent una vez si tiene al menos un tracker 'Working'
    # Ordenar torrents por nombre
    working_torrents.sort(key=lambda x: x.name)
    return working_torrents

# Función para contar torrents con trackers 'Not connect'
def get_not_connect_trackers():
    torrents = qb.torrents_info()
    not_connect_torrents = []
    for torrent in torrents:
        trackers = qb.torrents_trackers(torrent.hash)
        for tracker in trackers:
            if tracker['status'] == 1:
                not_connect_torrents.append(torrent)
                break  # Contamos el torrent una vez si tiene al menos un tracker 'Not connect'
    # Ordenar torrents por nombre
    not_connect_torrents.sort(key=lambda x: x.name)
    return not_connect_torrents

def generar_resumen():
    updating_trackers = get_updating_trackers()
    updating_count = len(updating_trackers)
    working_trackers = get_working_trackers()
    working_count = len(working_trackers)
    not_connect_trackers = get_not_connect_trackers()
    not_connect_count = len(not_connect_trackers) 
    message = f'📢 Resumen QBitTorrent'    
    ## send_telegram_message(message) 
    message_updating = f'Hay {updating_count} torrents con trackers "Updating".'
    ## send_telegram_message(message) 
    message_working = f'Hay {working_count} torrents con trackers "Working".'
    ## send_telegram_message(message) 
    message_not_connect = f'Hay {not_connect_count} torrents con trackers "Not connect".'
    message_resumen = message + '\n🟡 ' + message_updating + '\n🟢 ' + message_working + '\n🔴 ' + message_not_connect
    send_telegram_message(message_resumen)

    print(f'Torrents con trackers "Updating": {updating_count}')
    print(f'Torrents con trackers "Working": {working_count}')
    print(f'Torrents con trackers "Not connect": {not_connect_count}')   


# Función para enviar un mensaje a Telegram
def send_telegram_message_OLD(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    response.raise_for_status()

# Función para enviar mensajes a Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response   

# Función principal
def main(paused_threshold, not_working_threshold, include_name, include_resumen):
    try:
        # Intentar autenticar
        qb.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        error_message = f'Error de autenticación: {e}'
        print(error_message)
        send_telegram_message(error_message)
        return
    except qbittorrentapi.exceptions.APIConnectionError as e:
        error_message = f'Error de conexión con qBittorrent: {e}'
        print(error_message)
        send_telegram_message(error_message)
        return
    except Exception as e:
        error_message = f'Ocurrió un error: {e}'
        print(error_message)
        send_telegram_message(error_message)
        return

    try:
        # Comprobar si el número de torrents en pausa supera el umbral
        if paused_threshold > 0:
            paused_torrents = get_paused_torrents()
            paused_count = len(paused_torrents)
            if paused_count >= paused_threshold:
                if include_name:
                    torrent_names = '\n\n🟠 '.join(torrent.name for torrent in paused_torrents)
                    message = f'Hay {paused_count} torrents en pausa, parados o con error:\n\n🟠 {torrent_names}.'
                else:
                    message = f'Hay {paused_count} torrents en pausa, parados o con error.'
                send_telegram_message(message)
                if include_resumen:
                    generar_resumen()
                print(f'Mensaje enviado: {message}')
            else:
                print(f'Torrents en pausa, parados o con error: {paused_count}')

        # Comprobar si el número de torrents con trackers 'Not working' supera el umbral
        if not_working_threshold > 0:
            not_working_torrents = get_not_working_trackers()
            not_working_count = len(not_working_torrents)
            if not_working_count >= not_working_threshold:
                if include_name:
                    torrent_names = '\n\n🔴 '.join(torrent.name for torrent in not_working_torrents)
                    message = f'Hay {not_working_count} torrents con trackers "Not working":\n\n🔴 {torrent_names}.'
                else:
                    message = f'Hay {not_working_count} torrents con trackers "Not working".'
                send_telegram_message(message)
                if include_resumen:
                    generar_resumen()
                print(f'Mensaje enviado: {message}')
            else:
                print(f'Torrents con trackers "Not working": {not_working_count}')

      #  if include_resumen:
      #      generar_resumen()
    
    except requests.RequestException as e:
        error_message = f'Error al comunicarse con la API de Telegram: {e}'
        print(error_message)
        send_telegram_message(error_message)
    except Exception as e:
        error_message = f'Ocurrió un error: {e}'
        print(error_message)
        send_telegram_message(error_message)

if __name__ == '__main__':
    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(description='Monitorea torrents en qBittorrent y envía notificaciones a Telegram.')
    parser.add_argument('--pausado', type=int, default=1, help='Umbral de torrents en pausa para enviar notificación.')
    parser.add_argument('--no_tracker', type=int, default=1, help='Umbral de torrents con trackers "Not working" para enviar notificación.')
    parser.add_argument('--name', action='store_true', help='Incluir nombres de torrents en las notificaciones.')
    parser.add_argument('--resumen', action='store_true', help='Incluye un resumen con el estado de todos los torrents.')
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    # Inicializar el cliente qBittorrent
    qb = qbittorrentapi.Client(host=QB_IP, port=QB_PORT, username=QB_USER, password=QB_PASSWORD)
    
    # Llamar a la función principal con los valores de los argumentos
    main(args.pausado, args.no_tracker, args.name, args.resumen)