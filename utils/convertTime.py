def convertTime(time):
    pos = ['sn', 'dk', 'sa', 'gn']
    time_dict = {'sn': 1, 'dk': 60, 'sa': 3600, 'g': 3600*24}
    unit = time[-2::]
    print(unit)
    if unit not in pos:
        return -1
    try:
        val = int(time[:-2])
        print(val)
    except:
        return -2
    return val*time_dict[unit]
