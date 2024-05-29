import click
import re

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
    parse_dict = {}
    while data[0] != '}':
        values = string_parse(data)
        if not values:
            return None
        key,data = values

        values = colon_parse(data)
        if not values:
            return None
        _,data = values

        values = all_parse(data)
        if not values:
            return None
        value,data = values

        parse_dict[key] = value

        values = comma_parse(data)
        if not values:
            if data[0] != '}':
                return None
        _,data = values
    return (parse_dict,data.strip())


def find_ending_quote(data):
    escaped = False
    for i in range(len(data)):
        if escaped:
            escaped = False
            continue
        if data[i] == "\":
            escaped = True
        elif data[i] == '"':
            return i
    return -1

def array_parse(data):

def string_parse(data):
    if data[0] != '"':
        return None
    data = data[1:]
    end_quote_idx = find_ending_quote(data):
    if end_quote_idx == -1:
        return None
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
    return (value, data[:len(raw_value)].strip())

def comma_parse(data):
    if data[0] == ",":
        return (",", data[1:].strip())

def colon_parse(data):
    if data[0] == ":":
        return (":", data[1:].strip())

def all_parse(data):


@click.command()
@click.argument("file", nargs=1, type=click.Path(exists=True))
def parse():


    return 0

if __name__ == "__main__":
    parse()