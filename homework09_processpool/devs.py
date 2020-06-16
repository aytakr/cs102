import random

from ProcessPool import ProcessPool

def generate_matrix(size, N):
    arrays = []

    for arr in range(N):
        array1 = [[random.randint(0, 100) for i in range(size)] for i in range(size)]
        array2 = [[random.randint(0, 100) for i in range(size)] for i in range(size)]

        arrays.append((array1, array2))

    return arrays


def heavy_computation(arrays):
    new_matrix = [[0 for i in range(len(arrays[0]))] for i in range(len(arrays[0]))]

    for i in range(len(arrays[0])):
        for j in range(len(arrays[0])):
            for k in range(len(arrays[0])):
                new_matrix[i][j] += arrays[0][i][k] * arrays[1][k][j]

    return new_matrix



size = input('Enter size of square matrix: ')
N = input('How much matrix do you want? ')

big_data = generate_matrix(size, N)
pool = ProcessPool(2, 5, '1Gb')

results = pool.map(heavy_computation, big_data)

print('Working...')
for i in range(N):
    print('{} DATA CHUNK'.format(i+1))
    print('\nMatrix 1 is')
    print(big_data[i][0])
    print('\nMatrix 2 is')
    print(big_data[i][1])
    print('\nThe result is')
    print(results[i])
    print('\n\n')
