#!/bin/bash
chosen=$(printf "Выключить\nПерезагрузка\nСпящий режим\nВыйти\nЗаблокировать" | rofi -dmenu -p "Действие:")

case "$chosen" in
    "Выключить") systemctl poweroff ;;
    "Перезагрузка") systemctl reboot ;;
    "Спящий режим") hyprlock & systemctl suspend ;;
    "Выйти") hyprctl dispatch exit ;;  # для Hyprland
    "Заблокировать") hyprlock ;;       # или другой инструмент блокировки
esac
