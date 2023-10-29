def read_matrix(filename: str) -> list[list[float]]:
    '''Чтение матрицы nxm из файла filename'''
    with open(filename) as file:
        matrix = [list(map(float, row.split())) for row in file.readlines()]
    return matrix
