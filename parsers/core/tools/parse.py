import re


def remove_rnt(value: any) -> any:
    """
    Replace \r, \n, \t in string to one space.
    """
    if not value or not isinstance(value, str):
        return value
    value = value.replace('\x00', '')
    value = re.sub(r'\s', ' ', value)
    return re.sub(r'\s{2,}', ' ', value).strip()


def parse_int(value: any) -> any:
    """
    Return only number from string: '1 203 km' -> '1203'
    """
    if not value or not isinstance(value, str):
        return value
    clear_value = re.sub(r'\s', '', value)
    if result := re.search(r'\d+', clear_value):
        return result.group()


def parse_dotnum(value: any) -> any:
    """
    Return dotted number from string: '49.25 dollars' -> '49.25'
    """
    if not value or not isinstance(value, str):
        return value
    if clear_value := re.search(r'\d+\.\d{1,}', value):
        return clear_value.group()


def parse_comnum(value: any, default=None) -> any:
    """
     Return comma number from string: '49,25 dollars' -> '49,25'.
    """
    if not value or not isinstance(value, str):
        return value
    if clear_value := re.search(r'\d+,\d{1,}', value):
        return clear_value.group()


if __name__ == '__main__':
    print(parse_dotnum('1.33 usd'))
