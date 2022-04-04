
def float_range(start, end, step):
    val = start
    while val <= end:
        yield val
        val += step

