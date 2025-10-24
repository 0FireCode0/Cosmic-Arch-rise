#!/usr/bin/env python3
import argparse
import logging
import sys
import signal
import gi
import json
import time
from threading import Thread, Event

gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl, GLib

logger = logging.getLogger(__name__)

# Глобальные переменные для управления каруселью
current_text = ""  # Текущий текст для отображения
display_text = ""  # Текст, который сейчас показывается (с учетом карусели)
carousel_position = 0  # Текущая позиция в карусели
carousel_active = False  # Активна ли карусель
carousel_thread = None  # Поток для анимации карусели
stop_event = Event()  # Событие для остановки потока карусели
current_player = None  # Текущий активный плеер
scroll_delay = 0.375  # Задержка между обновлениями (в секундах) - уменьшено для плавности
silence_mode = False  # Флаг для отслеживания режима тишины

def write_output(text, player=None):
    logger.info('Writing output')

    # Если текст пустой, выводим пустую строку
    if not text:
        output = {'text': 'Тишина, холодна', 'class': '', 'alt': ''}
        sys.stdout.write(json.dumps(output) + '\n')
        sys.stdout.flush()
        return

    # Формируем выходные данные
    if player:
        output = {'text': text,
                  'class': 'custom-' + player.props.player_name,
                  'alt': player.props.player_name}
    else:
        output = {'text': text, 'class': 'silence', 'alt': 'silence'}

    sys.stdout.write(json.dumps(output) + '\n')
    sys.stdout.flush()

def start_carousel(text, player):
    """Запускает карусель для указанного текста"""
    global current_text, display_text, carousel_position, carousel_active, carousel_thread, stop_event, current_player

    # Останавливаем предыдущую карусель, если она активна
    stop_carousel()

    # Устанавливаем новые значения
    current_text = text + " | "
    display_text = text + " | "
    carousel_position = 0
    carousel_active = True
    current_player = player

    # Запускаем поток карусели
    stop_event.clear()
    carousel_thread = Thread(target=carousel_worker)
    carousel_thread.daemon = True
    carousel_thread.start()

    # Сразу обновляем вывод
    write_output(display_text, player)

def stop_carousel():
    """Останавливает карусель"""
    global carousel_active, stop_event

    carousel_active = False
    stop_event.set()
    if carousel_thread and carousel_thread.is_alive():
        carousel_thread.join(timeout=1)

def carousel_worker():
    """Рабочая функция для анимации карусели"""
    global display_text, carousel_position

    # Если текст короткий, не нужно анимировать
    if len(current_text) <= 30:
        return

    # Пауза перед началом анимации (2 секунды)
    time.sleep(0.5)

    while not stop_event.is_set():
        try:
            # Обновляем позицию карусели
            carousel_position = (carousel_position + 1) % len(current_text)

            # Формируем текст для отображения (30 символов)
            if carousel_position + 30 <= len(current_text):
                display_text = current_text[carousel_position:carousel_position+30]
            else:
                # Если достигли конца строки, продолжаем с начала
                remaining_chars = 30 - (len(current_text) - carousel_position)
                display_text = current_text[carousel_position:] + current_text[:remaining_chars]

            # Обновляем вывод
            if current_player:
                write_output(display_text, current_player)

            # Ждем перед следующим обновлением (уменьшено для плавности)
            stop_event.wait(scroll_delay)
        except Exception as e:
            logger.error(f"Error in carousel worker: {e}")
            break

def check_players_status(manager):
    """Проверяет статус плееров и выводит сообщение о тишине если нет активных"""
    global silence_mode, current_player
    
    if not manager.props.players:
        if not silence_mode:
            silence_mode = True
            write_output("Тишина, холодна")
    else:
        silence_mode = False

def on_play(player, status, manager):
    logger.info('Received new playback status')
    on_metadata(player, player.props.metadata, manager)
    check_players_status(manager)

def on_metadata(player, metadata, manager):
    logger.info('Received new metadata')
    global current_text, display_text, carousel_active, current_player

    track_info = ''

    if player.props.player_name == 'spotify' and \
            'mpris:trackid' in metadata.keys() and \
            ':ad:' in player.props.metadata['mpris:trackid']:
        track_info = 'AD PLAYING'
        stop_carousel()  # Останавливаем карусель для рекламы
        write_output(track_info, player)
    elif player.get_artist() != '' and player.get_title() != '':
        track_info = '{artist} - {title}'.format(artist=player.get_artist(),
                                                 title=player.get_title())
        # Запускаем карусель для длинного текста
        if len(track_info) > 30:
            start_carousel(track_info, player)
        else:
            stop_carousel()
            write_output(track_info, player)
    else:
        track_info = player.get_title()
        if track_info and len(track_info) > 30:
            start_carousel(track_info, player)
        else:
            stop_carousel()
            write_output(track_info, player)

    # Если плеер не воспроизводится, останавливаем карусель
    if player.props.status != 'Playing':
        stop_carousel()
        if track_info:
            write_output(track_info, player)

def on_player_appeared(manager, player, selected_player=None):
    if player is not None and (selected_player is None or player.name == selected_player):
        init_player(manager, player)
    else:
        logger.debug("New player appeared, but it's not the selected player, skipping")
    
    # Проверяем статус после появления плеера
    check_players_status(manager)

def on_player_vanished(manager, player):
    logger.info('Player has vanished')
    global current_player
    
    # Если исчез текущий плеер, останавливаем карусель
    if player == current_player:
        stop_carousel()
        current_player = None
    
    # Проверяем статус после исчезновения плеера
    check_players_status(manager)

def init_player(manager, name):
    logger.debug('Initialize player: {player}'.format(player=name.name))
    player = Playerctl.Player.new_from_name(name)
    player.connect('playback-status', on_play, manager)
    player.connect('metadata', on_metadata, manager)
    manager.manage_player(player)
    on_metadata(player, player.props.metadata, manager)

def signal_handler(sig, frame):
    logger.debug('Received signal to stop, exiting')
    stop_carousel()  # Останавливаем карусель при выходе
    sys.stdout.write('\n')
    sys.stdout.flush()
    sys.exit(0)

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Increase verbosity with every occurance of -v
    parser.add_argument('-v', '--verbose', action='count', default=0)

    # Define for which player we're listening
    parser.add_argument('--player')

    return parser.parse_args()

def main():
    arguments = parse_arguments()

    # Initialize logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                        format='%(name)s %(levelname)s %(message)s')

    # Logging is set by default to WARN and higher.
    # With every occurrence of -v it's lowered by one
    logger.setLevel(max((3 - arguments.verbose) * 10, 0))

    # Log the sent command line arguments
    logger.debug('Arguments received {}'.format(vars(arguments)))

    manager = Playerctl.PlayerManager()
    loop = GLib.MainLoop()

    manager.connect('name-appeared', lambda *args: on_player_appeared(*args, arguments.player))
    manager.connect('player-vanished', on_player_vanished)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for player in manager.props.player_names:
        if arguments.player is not None and arguments.player != player.name:
            logger.debug('{player} is not the filtered player, skipping it'
                         .format(player=player.name)
                         )
            continue

        init_player(manager, player)

    # Проверяем статус после инициализации всех плееров
    check_players_status(manager)

    try:
        loop.run()
    except KeyboardInterrupt:
        stop_carousel()
    finally:
        stop_carousel()

if __name__ == '__main__':
    main()
