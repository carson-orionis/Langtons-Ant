# <!-- ИСПОЛЬЗУЕМЫЕ МОДУЛИ --!>

from settings_data import *
from settings_handler import *
from structure_terrarium import *


# <!-- ИСПОЛЬЗУЕМЫЕ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ --!>

APPLICATION_CAPTION = "Langton's Ant"


# <!-- ОСНОВНОЙ АЛГОРИТМ РАБОТЫ ПРОГРАММЫ --!>

if __name__ == "__main__":
    # Получение значений параметров настроек приложения
    settings_handler = SettingsHandler(
        APPLICATION_CAPTION,
        SETTING_NAMES,
        SETTING_DATA_TYPES,
        SETTING_LIMITS,
        DEFAULT_SETTINGS)
    current_settings = settings_handler.get_settings_values()
    # Запуск жизненного цикла приложения
    current_session = Terrarium(
        current_settings['canvas_width'],
        current_settings['canvas_height'],
        current_settings['cell_side_lenght'],
        current_settings['framerate_cap'],
        current_settings['ant_count'],
        current_settings['music_file_format'],
        APPLICATION_CAPTION)
    current_session.launch_lifecycle()
