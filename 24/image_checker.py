from os import listdir
from os.path import isfile, join
from PIL import Image
from hopfield_nn_restore import read_in_file

names = [f for f in listdir('patterns') if isfile(join('patterns', f))]

input_vector = []
for name in names:

    path = 'patterns/' + name
    vector = list()
    with open(path) as file_object:
        for line in file_object:
            line = line.rstrip('\n')
            vector.append(line)
    input_vector.append(vector)

for i, elem in enumerate(input_vector):
    background = Image.new('RGBA', (len(elem[0]), len(vector)), (255, 255, 255, 255))
    width, height = background.size

    for x in range(height):
        for y in range(width):

            if elem[x][y] == '1':
                img = Image.new('RGB', (1, 1), color = (0, 0, 0))
                background.paste(img, (y, x))
            if elem[x][y] == '0':
                img = Image.new('RGB', (1, 1), color = (255, 255, 255))
                background.paste(img, (y, x))


    background.save(f'img/img_{name[i]}.png')
