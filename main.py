from file_reader import read_matrix
from petrov import *
from Job import * 
import sys

if __name__ == '__main__':
    # чтение из файла
    matrix = []
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f'Чтение из файла {filename}') 
        matrix = read_matrix(filename=filename)
    else:
        filename = input(f'Имя файла>: ')
        matrix = read_matrix(filename=filename)

    # конвертация данных в более удобный вид c вычислением p_1 и p_2
    calc_jobs = list_to_jobs(matrix)
    p = petrov(jobs=calc_jobs)

