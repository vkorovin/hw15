import datetime as dt

def is_valid_date(test_str,format="%d-%m-%Y"):
    try:
        result = bool(dt.datetime.strptime(test_str, format))
        return result
    except ValueError:
        return False


def is_today(str):
    today = dt.date.today().strftime('%d-%m')
    if dt.datetime.strptime(str,'%d-%m-%Y').strftime('%d-%m') == today:
        return True
    else:
        return False


if __name__== '__main__':
    print(is_valid_date('13-32-2022'))
    print(is_valid_date('13-01-2022'))
    print(is_today('18-07-1966'))
    print(is_today('08-07-1966'))

