def solution(N, M):
    days = 0
    stock = N
    while stock > 0:
        days += 1
        stock -= 1
        if days % M == 0:
            stock += 1
    return days