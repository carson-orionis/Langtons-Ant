# <!-- ИСПОЛЬЗУЕМЫЕ СТАНДАРТНЫЕ БИБЛИОТЕКИ --!>

from PIL import ImageGrab


# <!-- ИСПОЛЬЗУЕМЫЕ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ --!>

# Кортеж с названиями параметров настроек
SETTING_NAMES = (
    'canvas_width',
    'canvas_height',
    'cell_side_lenght',
    'framerate_cap',
    'ant_count',
    'music_file_format',
)

# Словарь типами значений параметров настроек
SETTING_DATA_TYPES = {
    SETTING_NAMES[0]:
        'int',
    SETTING_NAMES[1]:
        'int',
    SETTING_NAMES[2]:
        'int',
    SETTING_NAMES[3]:
        'int',
    SETTING_NAMES[4]:
        'int',
    SETTING_NAMES[5]:
        'str',
}

# Вычисление ширины и высоты дисплея компьютера, на котором было запущено данное
# приложение, с целью определения максимально воозможных ширины и высоты изобра-
# жения приложения, которое будет выводиться на экран.
IMAGE = ImageGrab.grab()
MAX_WIDTH = int(IMAGE.width * 0.9375)
MAX_HEIGHT = MAX_WIDTH // 2
del IMAGE

# Словарь с минимально и максимально возможными значениями параметров настроек
SETTING_LIMITS = {
    SETTING_NAMES[0]: {
        'Min':
            240,
        'Max':
            MAX_WIDTH,
    },
    SETTING_NAMES[1]: {
        'Min':
            240,
        'Max':
            MAX_HEIGHT,
    },
    SETTING_NAMES[2]: {
        'Min':
            0,
        'Max':
            2,
    },
    SETTING_NAMES[3]: {
        'Min':
            1,
        'Max':
            1080,
    },
    SETTING_NAMES[4]: {
        'Min':
            1,
        'Max':
            360,
    },
    SETTING_NAMES[5]: [
        'flac',
        'it',
        'mid',
        'mod',
        'mp3',
        'ogg',
        's3m',
        'wav',
        'xm',
    ],
}

# Значения параметров настроек по умолчанию
DEFAULT_SETTINGS = {
    SETTING_NAMES[0]:
        SETTING_LIMITS[SETTING_NAMES[0]]['Max'],
    SETTING_NAMES[1]:
        SETTING_LIMITS[SETTING_NAMES[1]]['Max'],
    SETTING_NAMES[2]:
        SETTING_LIMITS[SETTING_NAMES[2]]['Min'],
    SETTING_NAMES[3]:
        SETTING_LIMITS[SETTING_NAMES[3]]['Max'],
    SETTING_NAMES[4]:
        SETTING_LIMITS[SETTING_NAMES[4]]['Min'],
    SETTING_NAMES[5]:
        'mp3',
}
