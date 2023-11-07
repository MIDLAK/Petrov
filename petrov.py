from Job import Job, jobs_copy 
import math

def petrov(jobs: list[Job]) -> list[list[Job]]:
    '''Получение расписаний по правилам Петрова''' 
    D_0, D_1, D_2, D_01 = D_sets(jobs)
    D_012 = first_petrov(D_01=D_01, D_2=D_2)
    D = second_petrov(D_012=D_012) 
    third = third_petrov(D_1=D_1, D_0=D_0, D_2=D_2)
    fourth = fourth_petrov(D_1=D_1, D_2=D_2, D_0=D_0, D_01=D_01)

    return [D_012, D, third, fourth]


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
    объединением D_012 = D_01 + D_2''' # сортировка D_01 по возрастанию p_1
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


def fourth_petrov(D_1: list[Job], D_2: list[Job], 
                  D_0: list[Job], D_01: list[Job]) -> list[Job]:
    '''Производится упорядочивание по парам'''
    D_1_sorted_p1 = sorted(D_1, key=lambda job: job.p_1) 
    D_1_sorted_p2 = sorted(D_1, key=lambda job: job.p_2, reverse=True)

    D_0_sorted_p1 = sorted(D_0, key=lambda job: job.p_1) 
    D_0_sorted_p2 = sorted(D_0, key=lambda job: job.p_2, reverse=True)

    D_2_sorted_p1 = sorted(D_2, key=lambda job: job.p_1)
    D_2_sorted_p2 = sorted(D_2, key=lambda job: job.p_2, reverse=True)

    # формирование пар из D_1
    couples_D_1 = []
    for i in range(len(D_1)):
        if D_1_sorted_p1[i].index != D_1_sorted_p2[i].index:
            couples_D_1.append([D_1_sorted_p1[i], D_1_sorted_p2[i]]) 
        else:
            couples_D_1.append([D_1_sorted_p1[i], None])
    couples_D_1 = couples_D_1[:math.ceil(len(D_1)/2)]
    couples_D_1[0][0], couples_D_1[0][1] = couples_D_1[0][1], couples_D_1[0][0]

    # если количество деталей в D_1 нечётно (одна пара пустая)
    # то в полупустую пару добавляется элемент из D_0 или D_2
    if len(D_1) % 2 == 1:
        if len(D_0) != 0:
            couples_D_1[-1][1] = D_0_sorted_p1[0]
            D_0_sorted_p1.pop(0)
        elif len(D_2) != 0:
            couples_D_1[-1][1] = D_2_sorted_p1[0]
            D_2_sorted_p1.pop(0)

    # формирование пар из остатков D_0
    couples_D_0 = []
    for i in range(len(D_0_sorted_p1)):
        if D_0_sorted_p1[i].index != D_0_sorted_p2[i].index:
            couples_D_0.append([D_0_sorted_p1[i], D_0_sorted_p2[i]])
        else:
            couples_D_0.append([D_0_sorted_p1[i], None])

    # если количество деталей в D_0 нечётно (одна пара пустая)
    # то в полупустую пару добавляется элемент из D_2
    if len(D_0_sorted_p1) % 2 == 1:
        if len(D_2_sorted_p1) != 0:
            couples_D_0[-1][1] = D_2_sorted_p1[0]
            D_2_sorted_p1.pop(0)

    # формирование пар из остатков D_2
    couples_D_2 = []
    for i in range(len(D_2_sorted_p1)):
        if D_2_sorted_p1[i].index != D_2_sorted_p2[i].index:
            couples_D_2.append([D_2_sorted_p1[i], D_2_sorted_p2[i]])
        else:
            couples_D_2.append([D_2_sorted_p1[i], None])

    couples = [*couples_D_1, *couples_D_0, *couples_D_2]

    # вклинивание остатка если таковой имеется
    if couples[-1][1] == None:
        i_clin = 0
        lmbd_clin = couples[-1][0].p_2 - couples[-1][0].p_1
        for i in range(len(couples)-2):
            lmbd_i = max(couples[i][0].p_2 - couples[i][0].p_1,
                      couples[i][1].p_2 - couples[i][1].p_1)
            lmbd_next_i = min(couples[i+1][0].p_2 - couples[i+1][0].p_1,
                           couples[i+1][1].p_2 - couples[i+1][1].p_1)
            if  lmbd_clin < lmbd_i and lmbd_clin > lmbd_next_i:
                i_clin = i+1
        # вклинивание элемента
        couples.insert(i_clin, couples[-1])
        couples.pop()

    # избавление от парности
    result = []
    for coup in couples:
        result.append(coup[0])
        if coup[1] != None:
            result.append(coup[1])

    return result
