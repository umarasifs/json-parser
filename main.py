import click
import re
import sys

class InvalidJSON(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"{self.args[0]}"

def null_parse(data):
    if data[:4] == 'null':
        return (None,data[4:].strip())

def bool_parse(data):
    if data[:5] == 'false':
        return (False, data[5:].strip())
    elif data[:4] == 'true':
        return (True, data[4:].strip())


def object_parse(data):
    if data[0] != '{':
        return None
    data = data[1:].strip()
    parse_dict = {}

    if len(data) == 0:
        raise InvalidJSON("Incomplete Object",10)

    while data[0] != '}':
        values = string_parse(data)
        if not values:
            raise InvalidJSON("Invalid Object Key",11)
        key,data = values

        if len(data) == 0:
            raise InvalidJSON("Incomplete Object",10)

        values = colon_parse(data)
        if not values:
            raise InvalidJSON("Missing Colon",12)
        _,data = values

        if len(data) == 0:
            raise InvalidJSON("Incomplete Object",10)

        values = all_parse(data)
        if not values:
            raise InvalidJSON("Invalid Object Value",13)
        value,data = values

        if len(data) == 0:
            raise InvalidJSON("Incomplete Object",10)

        parse_dict[key] = value
        values = comma_parse(data)
        if not values:
            if data[0] != '}':
                raise InvalidJSON("Missing Closing }",14)
        else:
            _,data = values
            if len(data) == 0:
                raise InvalidJSON("Incomplete Object",10)
            if data[0] == '}':
                raise InvalidJSON("Extra Comma",15)
    return (parse_dict,data[1:].strip())


def find_ending_quote(data):
    escaped = False
    for i in range(len(data)):
        if escaped:
            escaped = False
            continue
        if data[i] == "\\":
            escaped = True
        elif data[i] == '"':
            return i
    return -1

def array_parse(data):
    if data[0] != '[':
        return None
    data = data[1:].strip()
    parse_array = []
    if len(data) == 0:
        raise InvalidJSON("Incomplete Array",20)
    while data[0] != ']':
        if len(data) == 0:
            raise InvalidJSON("Incomplete Array",20)
        values = all_parse(data)
        if not values:
            raise InvalidJSON("Invalid Array Value",21)
        value,data = values

        parse_array.append(value)

        if len(data) == 0:
            raise InvalidJSON("Incomplete Array",20)

        values = comma_parse(data)
        if not values:
            if data[0] != ']':
                raise InvalidJSON("Missing Closing ]",22)
        else:
            _,data = values
            if len(data) == 0:
                raise InvalidJSON("Incomplete Array",20)
            if data[0] == ']':
                raise InvalidJSON("Extra Comma",23)
    return (parse_array,data[1:].strip())

def string_parse(data):
    if data[0] != '"':
        return None
    data = data[1:]
    end_quote_idx = find_ending_quote(data)
    if end_quote_idx == -1:
        raise InvalidJSON("Missing Closing \"",30)
    return (bytes(data[:end_quote_idx], 'utf-8').decode('unicode_escape'), data[end_quote_idx+1:].strip())

def num_parse(data):
    number_regex = r'^[-+]?\b\d+(\.\d+)?([eE][-+]?\d+)?\b'
    match = re.search(number_regex,data)
    if not match:
        return None
    raw_value = match.group(0)
    value = float(raw_value)
    if value %1 == 0:
        value = int(value)
    return (value, data[len(raw_value):].strip())

def comma_parse(data):
    if data[0] == ",":
        return (",", data[1:].strip())

def colon_parse(data):
    if data[0] == ":":
        return (":", data[1:].strip())

def all_parse(data):
    values = null_parse(data)
    if values:
        return values
    values = bool_parse(data)
    if values:
        return values
    values = object_parse(data)
    if values:
        return values
    values = array_parse(data)
    if values:
        return values
    values = string_parse(data)
    if values:
        return values
    values = num_parse(data)
    if values:
        return values
    raise InvalidJSON("Invalid Format",2)

def initial_parse(data):
    values = object_parse(data)
    if values:
        if len(values[1]) != 0:
            raise InvalidJSON("Not An Array Or Object",1)
        return values
    values = array_parse(data)
    if values:
        if len(values[1]) != 0:
            raise InvalidJSON("Not An Array Or Object",1)
        return values
    raise InvalidJSON("Not An Array Or Object",1)

@click.command()
@click.argument("filename", nargs=1, type=click.Path(exists=True))
def parse(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            values = initial_parse(data)
            value, _ = values
    except InvalidJSON as e:
        print(f"Caught an exception: {e}")
        sys.exit(e.error_code)
    sys.exit(0)

if __name__ == "__main__":
    parse()