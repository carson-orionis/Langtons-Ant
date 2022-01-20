# <!-- ИСПОЛЬЗУЕМЫЕ СТАНДАРТНЫЕ БИБЛИОТЕКИ --!>

import random
import os
import sys
import time

# <!-- ИСПОЛЬЗУЕМЫЕ СКАЧИВАЕМЫЕ БИБЛИОТЕКИ --!>

import numpy
import pygame

# <!-- ИСПОЛЬЗУЕМЫЕ МОДУЛИ --!>

from string_case_handler import *
from structure_ant import *


# <!-- ИСПОЛЬЗУЕМЫЙ КЛАСС --!>

class Terrarium:
    """ Класс "Террариум". """

    # Название файла с фоновой музыкой (без формата)
    bgm_filename = 'bg_music'

    # Название папки для скриншотов, сделанных внутри приложения
    screenshots_path = 'screenshots'


    def __init__(self,
        width: int,
        height: int,
        cell_size: int,
        framerate: int,
        ant_count: int,
        music_format: str,
        app_caption: str) -> None:
        """
        Конструктор экземпляров объекта класса "Террариум".

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".
        width – ширина изображения в пикселях.
        height – высота изображения в пикселях.
        cell_size – длина стороны одной ячейки террариума в пикселях.
        framerate – ограничение максимальной частоты кадров.
        ant_count – количество муравьёв, которые будут бегать по террариуму.
        app_caption – название приложения, выводимое в заголовок окна.

        """
        self.framerate = framerate
        self.ant_count = ant_count
        self.app_caption = app_caption
        self.app_name = to_snake_case(self.app_caption)
        self.cell_size = 2 ** cell_size
        self.size_x = width // self.cell_size
        self.size_y = height // self.cell_size
        self.width = self.size_x * self.cell_size
        self.height = self.size_y * self.cell_size
        self.table = numpy.full((self.size_y, self.size_x), False, dtype=bool)
        self.__create_ants()
        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.canvas.fill(Ant.colors['clean'])
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        self.jukebox =  pygame.mixer.music
        self.music_file_path = ''.join([
            './',
            Terrarium.bgm_filename,
            '.',
            music_format,
        ])
        self.volume = 0.25
        self.paused = False
        pygame.display.flip()
        self.start_play_music()

    @staticmethod
    def __form_hue_spectre(start: int, finish: int, hue_count: int):
        """
        Статический приватный метод класса "Террариум", формирующий список равно-
        удалённых друг от друга значений оттенков заранее определённого количест-
        ва (необходимо для генерации списка муравьёв).

        Ключевые аргументы:
        start - начало спектра оттенков.
        finish - конец спектра оттенков.
        hue_count - необходимое количество значений оттенков.

        """
        spectre = []
        if hue_count == 1:
            spectre.append(random.randint(start, finish))
        elif hue_count == finish:
            for x in range(finish):
                spectre.append(x)
        else:
            part = finish // hue_count
            modulo = finish % hue_count
            x = random.randint(start, part+modulo)
            while len(spectre) < hue_count:
                spectre.append(x)
                x += part
        return spectre

    def __create_ants(self):
        """
        Метод экземпляра объекта класса "Террариум", формирующая список новых му-
        равьёв в заранее определённом количестве, которые будут бегать по терра-
        риуму.

        Используется в конструкторе экземпляров объекта класса.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        self.ant_list = []
        hue_list = Terrarium.__form_hue_spectre(
            Ant.colors['H_begin'], Ant.colors['H_end'], self.ant_count)
        for current_number in range(self.ant_count):
            self.ant_list.append(
                Ant(
                    random.randint(0, self.size_x-1),
                    random.randint(0, self.size_y-1),
                    hue_list[current_number]))

    def start_play_music(self):
        """
        Метод экземпляра объекта класса "Террариум", включающий воспроизведение
        фоновой музыки.

        Используется в конструкторе экземпляров объекта класса.

        поддерживаемые форматы музыкальных файлов:
        .flac, .it, .mid, .mod, .mp3, .ogg, .s3m, .wav, .xm
        (проверено)

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        if os.path.exists(self.music_file_path):
            self.jukebox.load(self.music_file_path)
            self.jukebox.play(loops=-1)
            self.jukebox.set_volume(self.volume)

    def make_screenshot(self):
        """
        Метод экземпляра объекта класса "Террариум", захватывающий кадр с проис-
        ходящим в окне приложения на данный момент (то бишь в момент нажатия со-
        ответствующей горячей клавиши) и сохраняющий его в графический файл фор-
        мата PNG.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        scrn_path = f'./{Terrarium.screenshots_path}'
        if not os.path.exists(scrn_path):
            os.mkdir(scrn_path)
        current_datetime = time.strftime("%Y-%m-%d_%H-%M-%S")
        pygame.image.save(
            self.canvas,
            f"{scrn_path}/{self.app_name}__{current_datetime}.png")

    def pause(self):
        """
        Метод экземпляра объекта класса "Террариум", ставящий процесс работы
        приложения вместе с воспроизведением музыки (если она есть) на паузу
        и снимающий всё это дело с паузы, если она уже поставлена.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        self.paused = not self.paused
        if self.paused:
            self.jukebox.pause()
            pygame.display.set_caption(self.app_caption)
        else:
            self.jukebox.unpause()

    def exit(self):
        """
        Метод экземпляра объекта класса "Террариум", завершающий процесс рабо-
        ты приложения.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """
        Метод экземпляра объекта класса "Террариум", обрабатывающий события, в
        том числе нажатия на горячие клавиши.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        for i in pygame.event.get():
            # Завершение работы приложения c закрытием окна приложения
            if i.type == pygame.QUIT:
                self.exit()
            # Установка процесса работы приложения на паузу при сворачивании окна
            # приложения
            if i.type == pygame.WINDOWMINIMIZED:
                if not self.paused:
                    self.pause()
            # Снятие процесса работы приложения с паузы при разворачивании окна
            # приложения
            if i.type == pygame.WINDOWRESTORED:
                self.pause()
            # Обработка горячих клавиш
            if i.type == pygame.KEYDOWN:
                # Завершение работы приложения при нажатии на клавишу "Escape"
                if i.key == pygame.K_ESCAPE:
                    self.exit()
                # Установка процесса работы приложения  на паузу при нажатии на
                # клавишу "Пробел" (снятие паузы на неё же)
                if i.key == pygame.K_SPACE:
                    self.pause()
                # Захват и сохранение скриншота на клавишу "Ввод"
                if i.key == pygame.K_RETURN:
                    self.make_screenshot()
                # Увеличение громкости фоновой музыки при нажатии на клавишу
                # "Стрелка Вверх"
                if i.key == pygame.K_UP:
                    self.volume += 0.05
                    self.jukebox.set_volume(self.volume)
                # Уменьшение громкости фоновой музыки при нажатии на клавишу
                # "Стрелка Вниз"
                if i.key == pygame.K_DOWN:
                    self.volume -= 0.05
                    self.jukebox.set_volume(self.volume)

    def recolor_cell(self, pos_x: int, pos_y: int, color):
        """
        Метод экземпляра объекта класса "Террариум", перекрашивающий одну ячейку
        террариума, находящуюся по полученным координатам, в новый цвет.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".
        pos_x - координаты перекрашиваемой ячейки по ширине изображения.
        pos_y - координаты перекрашиваемой ячейки по высоте изображения.
        color - новый цвет перекрашиваемой ячейки.

        """
        x = pos_x * self.cell_size
        y = pos_y * self.cell_size
        pygame.draw.rect(
            self.canvas,
            color,
            (x, y, self.cell_size, self.cell_size))

    def make_ants_turns(self):
        """
        Метод экземпляра объекта класса "Террариум", приводящий муравьёв в движе-
        ние: повороты влево/вправо, перемещение на следующую ячейку, перекрашива-
        ние ячеек в соответствии со значением цвета муравья.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        for current_ant in self.ant_list:
            new_color = current_ant.rotate(self.table)
            self.recolor_cell(
                current_ant.pos_x,
                current_ant.pos_y,
                new_color)
            new_color = current_ant.move(self.size_x, self.size_y)
            self.recolor_cell(
                current_ant.pos_x,
                current_ant.pos_y,
                new_color)

    def launch_lifecycle(self):
        """
        Метод экземпляра объекта класса "Террариум", описывающий жизненный цикл
        и работу приложения "Муравей Лэнгтона", а также все возможные с ним ин-
        теракции со стороны пользователя.

        Ключевые аргументы:
        self – экземпляр объекта класса "Террариум".

        """
        while True:
            self.handle_events()
            if not self.paused:
                self.clock.tick(self.framerate)
                self.make_ants_turns()
                pygame.display.flip()
                current_fps = self.clock.get_fps()
                pygame.display.set_caption(
                    f"{self.app_caption} (FPS: {int(current_fps)})")
