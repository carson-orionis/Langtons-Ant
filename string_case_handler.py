# <!-- ИСПОЛЬЗУЕМЫЕ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ --!>

base = tuple(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_ ')


# <!-- ИСПОЛЬЗУЕМЫЕ ПОДПРОГРАММЫ --!>

def to_base(source_string: str) -> str:
    """
    Функция удаления из строки символов, не являющихся большими или малыми буква-
    ми латинского алфавита, цифрами, пробелами, дефисами или знаками нижнего под-
    чёркивания.

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    result_string = f'{source_string}'
    strlen = len(result_string)
    i = 0
    while i < strlen:
        if not result_string[i] in base:
            if i == 0:
                result_string = result_string[i+1:]
            elif i == len(result_string)-1:
                result_string = result_string[:i]
            else:
                result_string = ''.join([
                    result_string[:i],
                    result_string[i+1:],
                ])
            strlen -= 1
        else:
            i += 1
    return result_string

def to_pascal_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид PascalCase.

    Пример:
    Frank Herbert's Dune -> FrankHerbertsDune

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return ''.join(to_base(source_string).title().split(' '))

def to_camel_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид camelCase.

    Пример:
    Frank Herbert's Dune -> frankHerbertsDune

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    result_string = to_pascal_case(source_string)
    return ''.join([result_string[0].lower(), result_string[1:]])

def to_kebab_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид kebab-case.

    Пример:
    Frank Herbert's Dune -> frank-herberts-dune

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return '-'.join(to_base(source_string).lower().split(' '))

def to_screaming_kebab_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид SCREAMING-KEBAB-CASE.

    Пример:
    Frank Herbert's Dune -> FRANK-HERBERTS-DUNE

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return '-'.join(to_base(source_string).upper().split(' '))

def to_train_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид Train-Case.

    Пример:
    Frank Herbert's Dune -> Frank-Herberts-Dune

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return '-'.join(to_base(source_string).title().split(' '))

def to_snake_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид snake_case.

    Пример:
    Frank Herbert's Dune -> frank_herberts_dune

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return '_'.join(to_base(source_string).lower().split(' '))

def to_screaming_snake_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид SCREAMING_SNAKE_CASE.

    Пример:
    Frank Herbert's Dune -> FRANK_HERBERTS_DUNE

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return '_'.join(to_base(source_string).upper().split(' '))

def to_camel_snake_case(source_string: str) -> str:
    """
    Функция преобразования строки в вид Camel_Shake_Case.

    Пример:
    Frank Herbert's Dune -> Frank_Herberts_Dune

    Ключевые аргументы:
    source_string – строка, которая будет преобразована.

    """
    return '_'.join(to_base(source_string).title().split(' '))
