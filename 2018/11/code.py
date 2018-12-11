import numpy as np
from PIL import Image
 
serial = 4151
cells = np.zeros((300, 300))
 
def get_hundreds_digit(n):
    return (n // 100) % 10
 
def get_power_level(x, y, serial):
    rackID = x + 10
    return get_hundreds_digit((rackID * y + serial) * rackID) - 5
 
xrange = list(range(0, 300))
yrange = list(range(0, 300))
for y in yrange:
    for x in xrange:
        cells[y][x] = get_power_level(x + 1, y + 1, serial)
 
def find_best_coord(cells, size):
    best_coord = (0, 0)
    max_power = -2147483648
    xrange = list(range(0, 300 - size + 1))
    yrange = list(range(0, 300 - size + 1))
    ixrange = list(range(0, size))
    iyrange = list(range(0, size))
    for y in yrange:
        for x in xrange:
            power = 0
            for iy in iyrange:
                for ix in ixrange:
                    power += cells[y + iy][x + ix]
            if power > max_power:
                max_power = power
                best_coord = (x + 1, y + 1)
    return best_coord, max_power
 
print(find_best_coord(cells, 3))
 
 # hell yea the bruteforce
def find_best_size(cells, lower, upper):
    max_power = -2147483648
    best_coord = (0, 0)
    best_size = 0
    for size in range(lower, upper + 1):
        print("Searching size", size)
        coord, power = find_best_coord(cells, size)
        print(coord, power)
        if power > max_power:
            max_power = power
            best_coord = coord
            best_size = size
    return (best_coord[0], best_coord[1], best_size), max_power
 
def create_image(cells):
    min_value = np.amin(cells)
    max_value = np.amax(cells)
    im = Image.new('RGB', cells.shape, "black")
    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            grey = int(round((cells[j][i] - min_value) / (max_value - min_value) * 255.0))
            pixels[i,j] = (grey, grey, grey)
    return im
 
create_image(cells).show()

# the average value is negative, so eventually the values will drop, stop manually
print(find_best_size(cells, 1, 300))