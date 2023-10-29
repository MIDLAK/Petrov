from Job import Job, jobs_copy

def petrov(jobs: list[Job]) -> list[Job]:
    '''Получение лучшего расписания по правилам Петрова'''
    D_0, D_1, D_2, D_01 = D_sets(jobs)
    D_012 = first_petrov(D_01=D_01, D_2=D_2)
    D = second_petrov(D_012=D_012)
    third = third_petrov(D_1=D_1, D_0=D_0, D_2=D_2)

def D_sets(jobs: list[Job]) -> tuple[list[Job], list[Job],
                                     list[Job], list[Job]]:
    '''Разбиение исходного множества на D_0, D_1, D_2 и D_01'''
    D_0 = [] # lambda = 0
    D_1 = [] # lambda > 0
    D_2 = [] # lambda < 0
    jobs_c = jobs_copy(jobs)
    for job in jobs_c:
        lmbd = job.p_2 - job.p_1
        if lmbd == 0:
            D_0.append(job)
        elif lmbd > 0:
            D_1.append(job)
        elif lmbd < 0:
            D_2.append(job)
    D_01 = [*D_0, *D_1]
    return (D_0, D_1, D_2, D_01)

def first_petrov(D_01: list[Job], D_2: list[Job]) -> list[Job]:
    '''Ранжирование D_01 по возарастанию p_1 и D_2 по убыванию p_2 c последующим
    объединением D_012 = D_01 + D_2'''
    # сортировка D_01 по возрастанию p_1
    sorted_D_01 = sorted(D_01, key=lambda job: job.p_1)
    # сортировка D_2 по убыванию p_2
    sorted_D_2 = sorted(D_2, key=lambda job: job.p_2, reverse=True)
    D_012 = [*sorted_D_01, *sorted_D_2]
    return D_012

def second_petrov(D_012: list[Job]) -> list[Job]:
    '''Ранжирование D_012 в порядке убывания lambda = p_2 - p_1'''
    return sorted(D_012, key=lambda job: job.p_2 - job.p_1, reverse=True)

def third_petrov(D_1: list[Job], D_0: list[Job], D_2: list[Job]) -> list[Job]:
    '''Ранжирование D_1 по возрастанию p_1, D_0 по возрастанию p_1, D_2 по убыванию p_2.
    Возвращается D_1 + D_0 + D_2'''
    sorted_D_1 = sorted(D_1, key=lambda job: job.p_1)
    sorted_D_0 = sorted(D_0, key=lambda job: job.p_1)
    sorted_D_2 = sorted(D_2, key=lambda job: job.p_2, reverse=True)
    return [*sorted_D_1, *sorted_D_0, *sorted_D_2]

def fourth_petrov(D_1: list[Job], D_2: list[Job], D_0: list[Job], D_01: list[Job]) -> list[Job]:
    pass
