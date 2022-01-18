# <!-- ИСПОЛЬЗУЕМЫЕ СТАНДАРТНЫЕ БИБЛИОТЕКИ --!>

import random
from colorsys import hsv_to_rgb


# <!-- ИСПОЛЬЗУЕМЫЙ КЛАСС --!>

class Ant:
    """ Класс "Муравей". """

    # Словарь с перечислением всех возможных направлений движения муравья
    directions = {
        'N': 0,  # north
        'E': 1,  # east
        'S': 2,  # south
        'W': 3   # west
    }

    # Словарь с перечислением всех возможных цветов муравья и его следов, а так-
    # же с цветом чистой ячейки поля
    colors = {
        'H_begin': 0,
        'H_end': 360,
        'S80': 80,
        'B50': 50,
        'B100': 100,
        'clean': (16, 16, 16),
    }


    def __init__(self, start_pos_x: int, start_pos_y: int, hue: int):
        """
        Конструктор экземпляров объекта класса "Муравей".

        Ключевые аргументы:
        self - экземпляр объекта класса "Муравей".
        start_pos_x - стартовое положение муравья на поле по горизонтали.
        start_pos_y - стартовое положение муравья на поле по вертикали.
        hue - значение тона цвета муравья, используемое для генерации цвета как
        самого муравья, так и оставляемых им следов.

        """
        self.pos_x = start_pos_x
        self.pos_y = start_pos_y
        self.direct = random.randint(
            Ant.directions['N'], Ant.directions['W'])
        self.ant_color = Ant.__hsv2rgb(
            hue,
            self.colors['S80'],
            self.colors['B50'])
        self.trace_color = Ant.__hsv2rgb(
            hue,
            self.colors['S80'],
            self.colors['B100'])

    @staticmethod
    def __hsv2rgb(hue: int, saturation: int, brightness: int):
        """
        Статический приватный метод класса "Муравей", генерирующий RGB-значения
        цвета на основе полученных на входе значений тона цвета, насыщенности и
        яркости (необходимо для получения значения цвета самого муравья и остав-
        ляемых им следов).

        Используется в конструкторе экземпляров объекта класса.

        Ключевые параметры:
        hue – значение тона цвета (от 0 до 360).
        saturation – значение насыщенности цвета (от 0 до 100).
        brightness – значение яркости цвета (от 0 до 100).

        """
        return tuple(round(x*255) for x in hsv_to_rgb(
            hue/360, saturation/100, brightness/100))

    def rotate(self, field):
        """
        Метод экземпляра объекта класса "Муравей", осуществляющий одну итерацию
        цикла оставления/затирания своих следов и поворота направо/налево в за-
        висимости от цвета ячейки, на которой сейчас находится муравей.

        Ключевые аргументы:
        self - экземпляр объекта класса "Муравей".
        field - таблица координат террариума, по которому бегает муравей.

        """
        # Очищение муравьём закрашенной ранее ячейки
        if field[self.pos_y][self.pos_x]:
            field[self.pos_y][self.pos_x] = False
            new_color = self.colors['clean']
            # Поворот налево
            self.direct -= 1
            if self.direct < self.directions['N']:
                self.direct = self.directions['W']
        # Закрашивание муравьём пустой ячейки
        else:
            field[self.pos_y][self.pos_x] = True
            new_color = self.trace_color
            # Поворот направо
            self.direct += 1
            if self.direct > self.directions['W']:
                self.direct = self.directions['N']
        # Возврат нового цвета ячейки
        return new_color

    def move(self, field_size_x: int, field_size_y: int):
        """
        Метод экземпляра объекта класса "Муравей", осуществляющий одну итерацию
        цикла перемещения муравья на соседнюю ячейку.

        Ключевые аргументы:
        self - экземпляр объекта класса "Муравей".
        field_size_x - ширина террариума, по которому бегает муравей.
        field_size_y - высота террариума, по которому бегает муравей.

        """
        # Шаг вверх
        if self.direct == self.directions['N']:
            self.pos_y -= 1
            if self.pos_y < 0:
                self.pos_y = field_size_y-1
        # Шаг вправо
        elif self.direct == self.directions['E']:
            self.pos_x += 1
            if self.pos_x >= field_size_x:
                self.pos_x = 0
        # Шаг вниз
        elif self.direct == self.directions['S']:
            self.pos_y += 1
            if self.pos_y >= field_size_y:
                self.pos_y = 0
        # Шаг влево
        elif self.direct == self.directions['W']:
            self.pos_x -= 1
            if self.pos_x < 0:
                self.pos_x = field_size_x-1
        # Возврат цвета муравья
        return self.ant_color
