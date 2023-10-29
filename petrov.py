from Job import Job, jobs_copy

def petrov(jobs: list[Job]) -> list[Job]:
    D_0, D_1, D_2, D_01 = D_sets(jobs)
    print(f'D_0 = {D_0}, \nD_1 = {D_1}, \nD_2 = {D_2}, \nD_01 = {D_01}')


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
