from datetime import datetime

def is_valid_date(test_str,format="%d-%m-%Y"):
    try:
        result = bool(datetime.strptime(test_str, format))
    except ValueError:
        result = False
    finally:
        return result

if __name__== '__main__':
    print(is_valid_date('13-32-2022'))