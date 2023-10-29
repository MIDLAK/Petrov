from typing import NamedTuple
from dataclasses import dataclass

@dataclass
class Job:
    index: int
    processing_times: list[float] # длительности обработки на каждой из машин
    p_1: float # параметр для правил Петрова
    p_2: float # параметр для правил Петрова

def list_to_jobs(matrix: list[list[float]]) -> list[Job]:
    '''Конвертация матрицы длительностей обработки в массив объектов Job'''
    jobs = []
    index = 0
    for times in matrix:
        index += 1
        jobs.append(Job(index=index, processing_times=times,
                        p_1=0, p_2=0))

    # вычисление p_1 и p_2
    calc_jobs = calculate_params(jobs)
    return calc_jobs

def calculate_params(jobs: list[Job]) -> list[Job]:
    '''Вычисляет p_1, p_2 для каждой из работ'''
    machine_count = len(jobs[0].processing_times)
    jobs_c = jobs_copy(jobs=jobs)
    for job in jobs_c:
        # вычисление p_1:
        p_1_sum = 0
        for i in range(int((machine_count + (machine_count % 2))/2)):
            p_1_sum += job.processing_times[i]

        # вычисление p_2
        p_2_sum = 0
        for i in range(int((machine_count + 1 + (machine_count % 2))/2)-1, machine_count):
            p_2_sum += job.processing_times[i]

        job.p_1 = p_1_sum
        job.p_2 = p_2_sum

    return jobs_c

def jobs_copy(jobs: list[Job]) -> list[Job]:
    '''Копирование списка работ'''
    jobs_copy = []
    for job in jobs:
        jobs_copy.append(Job(index=job.index,
                             processing_times=[*job.processing_times],
                             p_1=job.p_1,
                             p_2=job.p_2))
    return jobs_copy
