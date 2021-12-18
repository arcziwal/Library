def if_not_empty(element):
    if element not in ("", 0, " ", False, None):
        return True
    else:
        return False


def check_isbn(isbn_code):
    isbn_as_list = [i for i in isbn_code]
    for index, char in enumerate(isbn_as_list):
        if char == '-':
            isbn_as_list.pop(index)
    how_many_digits = len(isbn_as_list)
    if how_many_digits == 10:
        if check_10_digit_isbn(isbn_as_list):
            return True
    elif how_many_digits == 13:
        if _check_13_digit_isbn(isbn_as_list):
            return True
        else:
            return False


def check_10_digit_isbn(isbn_list):
    result = 0
    for index, digit in enumerate(isbn_list):
        if digit != 'X':
            try:
                isbn_list[index] = int(digit)
            except ValueError:
                return False
    index = 1
    while index < 10:
        result += (isbn_list[index - 1] * index)
        index += 1
    result = result % 11
    if result in range(10):
        if result == isbn_list[9]:
            return True
        else:
            return False
    elif result == 10:
        if isbn_list[9] == 'X':
            return True
        else:
            return False
    else:
        return False


def _check_13_digit_isbn(isbn_list):
    last_digit = isbn_list.pop(12)
    wages_list = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]
    result = 0
    for index, value in enumerate(isbn_list):
        isbn_list[index] = int(value)
    for digit, wage in zip(isbn_list, wages_list):
        # print(f"Cyfra {digit} razy waga {wage} równa się {digit * wage}")
        result += (digit * wage)
    print(result)
    result %= 10
    print(result)
    result = 10 - result
    print(result)
    if result == int(last_digit):
        return True
    elif result == 10 and int(last_digit) == 0:
        return True
    else:
        return False
