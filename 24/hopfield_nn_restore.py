def read_in_file(names, dir):

    # Создаем пустой массив
    input_vector = []

    for name in names:

        # Создаем массив строк из файла до переноса
        path = dir + name
        vector = list()
        with open(path) as file_object:
            for line in file_object:
                line = line.rstrip('\n')
                vector.append(line)

        # Превращаем полученный массив в строку
        new_vector = reduce((lambda x, y: x + y), vector)

        # Создаем массив нулей размера входной матрицы и заполняем
        # в соответсвии с заданными условиями
        v = np.empty(len(new_vector))
        for i in range(len(new_vector)):
            if new_vector[i] == '0':
                v[i] = -1
            else:
                v[i] = 1
        input_vector.append(v)

    # Добавляем значения каждой матрицы в общий массив
    input_vector = np.asarray(input_vector)
    return input_vector, len(line)

#  Транспонирование матрицы
def transpose(vector):

    n = len(vector)
    trans_vector = np.zeros((n, 1))

    for i in range(n):
        trans_vector[i] = vector[i]

    return trans_vector


def calc_W(input_vector):

    n = len(input_vector[0])
    m = len(input_vector)
    W = np.zeros((n, n))

    for l in range(m):
        W += input_vector[l]*transpose(input_vector[l])

    for i in range(n):
        for j in range(n):
            if i == j:
                W[i, j] = 0

    return W

def testing(inc_vector, W, input_vector, ll):

    n = len(inc_vector)
    net = np.empty(n)

    for k in range(n):
        for j in range(n):
            net[k] += W[j, k]*inc_vector[j]

        if net[k] > 0: net[k] = 1
        if net[k] < 0: net[k] = -1
        if net[k] == 0: net[k] = inc_vector[k]

    # Тестирование на соответсвие известным векторам
    m = len(input_vector)
    num = 0
    for i in range(m):
        if np.array_equal(input_vector[i], net) == True:
            num = i + 1

    if num == 1: word = 'I'
    elif num == 2: word = 'C'
    elif num == 3: word = 'B'

    if num != 0:
        print_pattern([net], ['restored'], ll)
        print('\nВосстановленному образцу соответсвует образец: "', word,'"\n')
    else:
        print('\nВосстановить образ не удалось!')

# Функция для красивого вывода образ на экран
def print_pattern(pattern, name, ll):

    for i, elem in enumerate(pattern):
        print(f"\npattern: {name[i].replace('.txt', '').upper()}")
        img = ''
        for num, j in enumerate(elem):
            if num % ll == 0:
                img += '\n'
            if j == -1.:
                img += '0'
            elif j == 1.:
                img += '1'
        print(img)



if __name__ == '__main__':

    import numpy as np
    from functools import reduce
    from os import listdir
    from os.path import isfile, join

    # Достаем все файлы из папки patterns
    names = [f for f in listdir('patterns') if isfile(join('patterns', f))]
    print(f'\n* Список файлов в дирректории patterns: \n{names}\n')

    # Создаем массив входных веткоров
    input_vectors, len_line = read_in_file(names, 'patterns/')
    print_pattern(input_vectors, names, len_line)

    #  Создаем матрицуесовых коэффициентов
    W = calc_W(input_vectors)
    print(f'\n* Матрица весовых коэффициентов: {W}')

    #  Подадим искаженный образ
    inc_name = [f for f in listdir('inc') if isfile(join('inc', f))]
    inc_vector, len_line = read_in_file(inc_name, 'inc/')
    print_pattern(inc_vector, inc_name, len_line)

    # Распознаем образ
    testing(inc_vector[0], W, input_vectors, len_line)
