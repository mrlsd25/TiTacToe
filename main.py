import numpy
import random

# Размерность игрового поля
map_dimension = 3

"""Создаем матрицу игрового поля
0 - пустое значение, 1 - крестик (Х) , -1 - нолик (0)
"""
map_array = [[0 for x in range(map_dimension)] for y in range(map_dimension)]

# Знак игрока, которым он хочет играть. 1 - крестик, -1 - нолик
player_sign = 1


# Вывод игрового поля на экран. Аргумент - матрица игрового поля
def show_map(map_arr):
    # Построчный вывод игрового поля. 0-ая строка - заголовок
    print("#" * 40)
    print(" ", " ".join(map(str, range(1, len(map_array) + 1))))

    for i in range(len(map_arr)):
        # str_out - текущая строка для вывода
        # При выводе строки матрицы преобразовываем числовые значения в графические - крестики и нолики
        str_out = str(i + 1) + " " + format_str_out(" ".join(map(str, map_arr[i])))

        print(str_out)


# Форматирование строки для вывода на экран. Замена числовых значений матрицы на юзерфрендли - крестики и нолики.
def format_str_out(str_text):
    str_out = str(str_text).replace("0", '-')
    str_out = str_out.replace("-1", '0')
    str_out = str_out.replace("1", 'X')
    return str_out


# Ход игрока. Возвращает список строка и столбец, куда пользователь хочет поставить свой знак
def players_turn():
    print("Ваш ход.")
    # Получаем значение строки и столбца, куда игрок поставит свой знак
    row = input_int("Введите номер строки: ")
    col = input_int("Введите номер столбца: ")
    return [row, col]


# Ввод данных с проверкой. Должно быть только целое число и не больше размерности матрицы. Аругмент - строка запроса
def input_int(text):
    while True:
        try:
            x = int(input(text))
            if x > map_dimension:
                print("Число первышает допустимое!")
                continue
            # Матрица начинает счет с 0, поэтому все значения должны быть на 1 меньше
            return x - 1
        except ValueError:
            print("Вы ввели не целое!")


""""Проверка занята или нет позиция в матрице для хода. 
Аргументы:координаты проверяемой позиции (список), 2d матрица поля
Возвращает True - если занято"""
def check_position_bizy(coordinates, map_arr):
    if map_arr[coordinates[0]][coordinates[1]] != 0: return True
    return False


# Проверка на выигрыш. Возвращает -1 - в случае победы Ноликов, 1 - в случае победы крестиков. 0 - нет победы
def check_win(map_arr):
    """Проверка диагоналей
    Проверяем сумму основной диагонали
    Если сумма всех элементов кратна размерности матрицы,
        значит все элементы одинаковые. Делим сумму на количество элементов и возвращаем индекс победителя
        1 - крестики, -1 - нолики"""
    if numpy.trace(map_arr) != 0 and numpy.trace(map_arr) % len(map_arr) == 0:
        return numpy.trace(map_arr) / len(map_arr)
    # Зеркалим матрицу, для вычисления антидиагонали
    mirr_map_arr = numpy.fliplr(map_arr)
    if numpy.trace(mirr_map_arr) != 0 and numpy.trace(mirr_map_arr) % len(mirr_map_arr) == 0:
        return numpy.trace(mirr_map_arr) / len(mirr_map_arr)

    # Транспонируем матрицу, чтобы проверить столбцы на выигрыш
    t_map_arr = numpy.transpose(map_arr)

    for i in range(len(map_arr)):
        """Проверка строки на выигрыш. """
        if sum(map_arr[i]) != 0 and sum(map_arr[i]) % len(map_arr) == 0:
            return sum(map_arr[i]) / len(map_arr)
        # Провекра столбцов на выигрыш
        if sum(t_map_arr[i]) != 0 and sum(t_map_arr[i]) % len(t_map_arr) == 0:
            return sum(t_map_arr[i]) / len(t_map_arr)

    return 0


# Проверяем исчерпание возможных ходов. Аргумент - матрица игрового поля. Возвращаемое значение False - ходы еще есть.
#       True - ходы исчерпаны.
def check_terminate(map_arr):
    for i in range(len(map_arr)):
        # Если хотя бы один элемент строки равен 0, значит ходы есть, возвращаем False
        if not all(map_arr[i]): return False
    return True


# Ход компьютера. Аргумент - матрица игрового поля, знак игрока-противника(которым он играет).
# Возвращаемое значение, координаты хода компьюетра - список [x,y].
def pc_turn(map_arr, pl_sign):
    """ Ищем возможные завршения партии,
        для этого вызываем функцию поиска угрозы, в качестве второго аругмента передаем число(знак),
        которым играет компьютер."""
    result = check_throat(map_arr, pl_sign * (-1))
    if not result is None:
        return result

    """ Ищем угрозы. В качестве второго аргумента передаем число(знак), которым играет противник"""
    result = check_throat(map_arr, pl_sign)
    # Если результат отличен от None, есть угроза, возвращается значение ячейки, которую нужно закрыть.
    if not result is None:
        return result


    #Генерируем случайный индекс ячейки
    while True:
        i, j = random.randint(0,len(map_arr)-1), random.randint(0,len(map_arr)-1)
        if map_arr[i][j] == 0: return [i,j]


# Проверка угроз. Аргумент - матрица игрового поля, знак игрока-противника(которым он играет)
# Возвращает None, если угроз нет, или номер ячейки, в которую нужно поместить значние, чтоб не проиграть.
def check_throat(map_arr, pl_sign):
    """Проверяем диагонали. Если в сумме элементов диагонали не хватает только 1(или -1),
    чтоб стать кратным размерности матрицы, значит есть угроза проигрыша."""
    if (numpy.trace(map_arr) + pl_sign) != 0 and (numpy.trace(map_arr) + pl_sign) % len(map_arr) == 0:
        # Ищем свободную ячейку
        for i in range(len(map_arr)):
            # Если значение ячейки 0, значит она пустая, возвращаем ее
            if map_arr[i][i] == 0: return [i, i]

    # Зеркалим матрицу, для проверки антидиагонали.
    mirr_map_arr = numpy.fliplr(map_arr)
    if (numpy.trace(mirr_map_arr) + pl_sign) != 0 and (numpy.trace(mirr_map_arr) + pl_sign) % len(mirr_map_arr) == 0:
        # Ищем свободную ячейку
        for i in range(len(mirr_map_arr)):
            # Если значение ячейки 0, значит она пустая, возвращаем ее !!! с трюком -  у нас ведь зеркальная матрица.
            if mirr_map_arr[i][i] == 0: return [i, len(mirr_map_arr) - 1 - i]

    # Проверяем на угрозу строки матрицы и столбцы (через транспонированную матрицу).
    t_map_arr = numpy.transpose(map_arr)
    for i in range(len(map_arr)):
        if sum(map_arr[i]) + pl_sign != 0 and (sum(map_arr[i]) + pl_sign) % len(map_arr[i]) == 0:
            # Ищем свободную ячейку
            for j in range(len(map_arr[i])):
                if map_arr[i][j] == 0: return [i, j]

        # Поиск по столбцам в транспонированной матрице.
        if sum(t_map_arr[i]) + pl_sign!= 0 and (sum(t_map_arr[i]) + pl_sign) % len(t_map_arr[i]) == 0:
            # Ищем свободную ячейку
            for j in range(len(t_map_arr[i])):
                # Возвращаем переставленные значения, матрица ведь транспонированная.
                if t_map_arr[i][j] == 0: return [j, i]


while True:

    # Выводим на экран игроевое поле.
    show_map(map_array)
    # Запрашиваем ход игрока.
    players_coordinate = players_turn()
    # Проверяем, занята ли ячейка поля.
    if check_position_bizy(players_coordinate, map_array):
        print("Ячейка уже занята. Выберите другую!")
        continue
    # Вносим в матрицу ход игрока.
    map_array[players_coordinate[0]][players_coordinate[1]] = player_sign

    # Проверяем на выигрыш.
    win_result = int(check_win(map_array))
    if win_result:
        print(f"Победили: {format_str_out(win_result)}")
        break

    # Проверяем исчерпание ходов.
    if check_terminate(map_array):
        print("Ходов больше нет. Ничья.")
        break

    # Ход компьютера
    pc_coordinate = pc_turn(map_array, player_sign)
    map_array[pc_coordinate[0]][pc_coordinate[1]] = (-1) * player_sign

    # Проверяем на выигрыш.
    win_result = int(check_win(map_array))
    if win_result:
        print(f"Победили: {format_str_out(win_result)}")
        break

    # Проверяем исчерпание ходов.
    if check_terminate(map_array):
        print("Ходов больше нет. Ничья.")
        break

# Выводим на экран игроевое поле.
show_map(map_array)
