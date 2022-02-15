import json
import os


class EmptyRecords(Exception):
    pass


class FileNotFound(Exception):
    pass


def read_file(path, key_value, slice=5):
    KNOWN_KEYS = ("Previous records", "User text", "all")

    if not os.path.isfile(path):
        raise FileNotFound

    if key_value not in KNOWN_KEYS:
        raise TypeError(f"Unknown Record: specify a record that is in {KNOWN_KEYS}")

    if slice < 0 or slice > 7:
        raise TypeError("Invalid slice number")

    if key_value == "all":
        with open(path, 'r') as user_records:
            previous_state = json.load(user_records)
        return previous_state

    with open(path, 'r') as user_records:
        previous_state = json.load(user_records)
        if slice >= len(previous_state[key_value]):
            previous_state = previous_state[key_value]
        elif slice < len(previous_state[key_value]):
            previous_state = previous_state[key_value][:slice]

    if previous_state == []:
        raise EmptyRecords("No Previous Records")

    return previous_state


def write_file(path, key_value, user_data):
    KNOWN_KEYS = ("Previous records", "User text")

    if key_value not in KNOWN_KEYS:
        raise TypeError(f"Unknown Record: specify a record that is in {KNOWN_KEYS}")

    try:
        previous_state = read_file(path, key_value="all")
    except IOError:
        previous_state = {
            'Previous records': [],
            'User text': []
        }

    previous_state[key_value].append(user_data)

    with open(path, 'w+') as user_records:
        json.dump(previous_state, user_records, indent=4)


def create_file(path):
    state = {
            'Previous records': [],
            'User text': [],
    }
    with open(path, 'w+') as user_records:
        json.dump(state, user_records, indent=4)
