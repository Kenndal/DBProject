
def time_converter(_time):
    '09:59:14'
    _hh = _time[0:2]
    _mm = int(_time[3:5])
    mm = float(_mm)/60
    if mm < 0.1:
        mm = '0' + str(mm*10)[0:1]
    else:
        mm = str(mm*100)[0:2]
    new_time = _hh + '.' + mm
    return float(new_time)


if __name__ == '__main__':
    _time = '09:07:14'
    kek = time_converter(_time)
    print kek