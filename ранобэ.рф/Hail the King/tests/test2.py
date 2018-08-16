a = 'Глава 396.55 Убивает как'


def str_to_int(string: str):
    result = ''
    for i in string:
        try:
            int(i)
        except ValueError:
            continue
        result += i
    return int(result)


print(str_to_int(a))


def num(s):
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l


print(num(a))
