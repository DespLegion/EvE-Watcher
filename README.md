# EVE Watcher

### Простой Discord бот, умеющий создавать embed таймера структур и выдавать информацию по конкретным структурам

## Установка, настройка и запуск приложения:
1) Создать приложение (бота) на [discord.com/developers](https://discord.com/developers/applications/)
2) Создать директорию проекта
3) Склонировать этот репозиторий в созданную директрию
4) Создать виртуальное окружение (`python3 -m venv <myenvname>`)
5) Активировать виртуальное окружение (Win: `.\venv\Scripts\activate`, Lin: `source venv/bin/activate`)
6) Установить зависимости (`pip install -r requirements.txt`)
7) Заполнить `config.py`
8) Запустить `core.py` (В фоне: Win - `pythonw core.py`)

## Автозапуск
### Windows
1) Создать .bat файл
2) Прописать в файле путь до `python.exe` (для запуска в фоне `pythonw.exe`) из виртуального окружения. Пример: `D:\"project name"\"env name"\Scripts\python.exe` Далее через пробел прописать путь до `core.py`
3) Пример: 
```
@echo off
D:\TimerWatcher\venv\Scripts\pythonw.exe D:\TimerWatcher\core.py
```
4) Добавить .bat файл в автозагрузку или в планировщик задач Windows

### Linux
1) Создайте systemd файл проета по пути `/lib/systemd/system/"project name".service`
2) Пример заполнения 
``` 
[Unit]
Description="description"

[Service]
Type=simple
ExecStart="python venv path" "core.py path"

[Install]
WantedBy=multi-user.target
```
3) После создания/изменения systemd файла необходимо перезапустить демона: `sudo systemctl daemon-reload`
4) Запустите сервис командой `sudo systemctl start "project name".service`

## Инициализация бота

1) Назначить каналы для таймеров командами: `timer_create_channel` и `timer_ping_channel`
2) Готово :) 

#### Пример информации о структуре:

![](https://i.ibb.co/X58Gr0h/info.jpg)

#### Пример таймера:

![](https://i.ibb.co/Kyy8GB6/timer.jpg)


## Список команд:

1) `w_help` - Общий список команд
2) `info` - Информация о структуре
3) `timer` - Создать таймер. Доступна только в назначенном канале
4) `w_help_admin` - Список административных команд. Доступна только администратору сервера
5) `timer_create_channel` - Назначение канала для создания таймеров. Доступна только администратору сервера
6) `timer_ping_channel` - Назначение канала для оповещений (Пингов). Доступна только администратору сервера
7) `reset_channels` - Снять назначение со всех каналов. Доступна только администратору сервера
8) `update_systems` - Обновить базу солнечных систем через ESI. Доступна только администратору сервера
9) `shutdown` - Отключение бота (завершение работы скрипта на сервере). Доступна только владельцу бота

version 0.1.1