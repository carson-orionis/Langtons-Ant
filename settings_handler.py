# <!-- ИСПОЛЬЗУЕМЫЕ СТАНДАРТНЫЕ БИБЛИОТЕКИ --!>

import os
from configparser import *

# <!-- ИСПОЛЬЗУЕМЫЕ МОДУЛИ --!>

from string_case_handler import *


# <!-- ИСПОЛЬЗУЕМЫЙ КЛАСС --!>

class SettingsHandler:
    """ Класс "Обработчик настроек". """

    def __init__(self,
        application_name: str,
        settings_names: list,
        settings_data_types: dict,
        settings_limits: dict,
        default_settings: dict) -> None:
        """
        Конструктор экземпляров объекта класса "Обработчик настроек".

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".
        application_name – название приложения в исходном формате.
        settings_names – список названий параметров настроек приложения.
        settings_data_types – типы значений параметров настроек приложения.
        settings_limits – диапазоны допустимых значений параметров настроек при-
        ложения.
        default_settings – значения параметров настроек приложения по умолчанию.

        """
        self.__get_ini_names(application_name)
        self.settings_names = settings_names
        self.settings_data_types = settings_data_types
        self.settings_limits = settings_limits
        self.default_settings = default_settings
        self.config_parser = ConfigParser()

    def __get_ini_names(self, application_name: str) -> None:
        """
        Приватный метод экземпляра объекта класса "Обработчик настроек", генери-
        рующий название путь к .ini-файлу, содержащему значения параметров наст-
        роек приложения, и название внутреннего заголовка настроек.

        Используется в конструкторе экземпляров объекта класса.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".
        application_name – название приложения в исходном формате.

        """
        snake_case_app_name = to_snake_case(application_name)
        self.settings_filename = ''.join([
            './',
            snake_case_app_name,
            ".ini",
        ])
        self.settings_header = ''.join([
            snake_case_app_name,
            "__settings",
        ])

    def read_ini(self) -> None:
        """
        Метод экземпляра объекта класса "Обработчик настроек", считывающий значе-
        ния параметров настроек приложения из .ini-файла и сохраняющий их в виде
        словаря.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".

        """
        self.settings = dict.fromkeys(self.settings_names)
        self.config_parser.read(self.settings_filename)
        for current_setting in self.settings_names:
            if self.settings_data_types[current_setting] in 'str':
                self.settings[current_setting] = self.config_parser.get(
                    self.settings_header, current_setting)
            elif self.settings_data_types[current_setting] in 'int':
                self.settings[current_setting] = self.config_parser.getint(
                    self.settings_header, current_setting)
            elif self.settings_data_types[current_setting] in 'float':
                self.settings[current_setting] = self.config_parser.getfloat(
                    self.settings_header, current_setting)
            elif self.settings_data_types[current_setting] in 'bool':
                self.settings[current_setting] = self.config_parser.getbool(
                    self.settings_header, current_setting)

    def rewrite_ini(self, save_settings) -> None:
        """
        Метод экземпляра объекта класса "Обработчик настроек", полностью переза-
        писывающий содержимое .ini-файла.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".

        """
        save_settings_dict = {
            self.settings_header:
                save_settings
        }
        self.config_parser.read_dict(save_settings_dict)
        with open(self.settings_filename, 'wt', encoding='UTF-8') as config_file:
            self.config_parser.write(config_file)

    def update_ini(self, setting_name, setting_value) -> None:
        """
        Метод экземпляра объекта класса "Обработчик настроек", перезаписывающий
        в .ini-файле значение одного из параметров настроек приложения на новое.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".
        setting_name - название параметра настроек, значение которого будет пере-
        записано.
        setting_value - новое значение параметра настроек.

        """
        self.config_parser.read(self.settings_filename)
        self.config_parser[self.settings_header][setting_name] = setting_value
        with open(self.settings_filename, 'wt', encoding='UTF-8') as config_file:
            self.config_parser.write(config_file)

    def make_default_ini(self) -> None:
        """
        Метод экземпляра объекта класса "Обработчик настроек", перезаписывающий
        .ini-файл со значениями параметров настроек по умолчанию... Или создаю-
        щий этот файл при его отсутствии с последующей записью в него вышеназван-
        ного содержимого.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".

        """
        self.settings = self.default_settings.copy()
        self.rewrite_ini(self.settings)

    def setting_limits_check(self) -> None:
        """
        Метод экземпляра объекта класса "Обработчик настроек", проверяющий сло-
        варь со значениями параметров настроек приложения на соответствие допус-
        тимым диапазонам значений: при нахождении несоответствия происходит пе-
        резапись значения на допустимое как в словаре, так и в .ini-файле.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".

        """
        upd_list = dict.fromkeys(self.settings_names)
        for current_setting in self.settings:
            current_setting_value = self.settings[current_setting]
            if self.settings_data_types[current_setting] in 'str':
                current_setting_list = self.settings_limits[current_setting]
                cur_condit = current_setting_value in current_setting_list
                if cur_condit:
                    upd_list[current_setting] = current_setting_value
                else:
                    upd_list[current_setting] = self.default_settings[current_setting]
            elif (self.settings_data_types[current_setting] in 'int' or
                  self.settings_data_types[current_setting] in 'float'):
                current_setting_min = self.settings_limits[current_setting]['Min']
                current_setting_max = self.settings_limits[current_setting]['Max']
                cur_min_condit = current_setting_value >= current_setting_min
                cur_max_condit = current_setting_value <= current_setting_max
                if cur_min_condit and cur_max_condit:
                    upd_list[current_setting] = current_setting_value
                elif not cur_min_condit:
                    upd_list[current_setting] = current_setting_min
                elif not cur_max_condit:
                    upd_list[current_setting] = current_setting_max
        if upd_list != self.settings:
            self.settings = upd_list
            self.rewrite_ini(self.settings)

    def get_settings_values(self) -> dict:
        """
        Метод экземпляра объекта класса "Обработчик настроек", считывающий и воз-
        вращающий словарь со значениями параметров настроек приложения при усло-
        вии, что .ini-файл был считан без проблем, а словарь прошёл проверку на
        соответствие диапазонам допустимых значений параметров настроек, иначе он
        будет откорректирован вместе с .ini-файлом.

        Ключевые аргументы:
        self – экземпляр объекта класса "Обработчик настроек".

        """
        if os.path.isfile(self.settings_filename):
            try:
                self.read_ini()
            except:
                self.make_default_ini()
            else:
                self.setting_limits_check()
        else:
            self.make_default_ini()
        return self.settings
