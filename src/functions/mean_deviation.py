def calculate_mean_deviation(lst, sma_point):
    temp_num = 0
    for j in lst:
        temp_num += abs(sma_point - j)
    temp_num /= len(lst)
    if temp_num == 0:
        temp_num = 0.0000000001
    return temp_num