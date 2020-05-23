def reproduction_rate(values, index):
    if index < 4:
        return None
    latest = values[index]
    reference = values[index-4]
    if reference and reference != 0 :
        return min(latest / reference, 4)
    else:
        return None


def four_days_average(values, index):
    if index >= 3:
        return sum(values[index-3:index+1])/4
    else:
        return None

