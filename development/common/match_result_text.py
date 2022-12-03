import json

from development.constants import (
    ACTION,
    DIRECTION,
    FROM_COL,
    FROM_ROW,
    PLAYER_1,
    PLAYER_2,
    ROW_SIZE,
    SCORE_1,
    SCORE_2,
    TURNS
)


def add_text_if_data(data):
    eol = '\n'
    inner_data = json.loads(data['data']) if "data" in data else {}
    parsed_data = (
        f"---------------------------- Player Command -------------------------------------{eol}"
        f"{ f'Action: {data[ACTION]}{eol}' if ACTION in data else ''}"
        f"{ f'Coordinates: { inner_data[FROM_ROW]}, { inner_data[FROM_COL]}{eol}' if inner_data else ''}"
        f"{ f'Direction: {inner_data[DIRECTION]}{eol}{eol}' if inner_data else ''}"
    )

    return parsed_data


def add_text_if_not_data(log_data):

    eol = '\n'
    parsed_data = (
        f"--------------- Resulting Discovered Board after Player Command ------------------{eol}"
        f"{ f'Player 1 Score: {log_data[SCORE_1]}{eol}' if SCORE_1 in log_data else ''}"
        f"{ f'Player 2 Score: {log_data[SCORE_2]}{eol}' if SCORE_2 in log_data else ''}"
        f"{ f'Player 1 Name: {log_data[PLAYER_1]}{eol}' if PLAYER_1 in log_data else ''}"
        f"{ f'Player 2 Name: {log_data[PLAYER_2]}{eol}' if PLAYER_2 in log_data else ''}"
        f"{ f'Remaining turns: {log_data[TURNS]}{eol}' if TURNS in log_data else ''}"
        f"{ f'Last command coords: {log_data[FROM_ROW]}, {log_data[FROM_COL]}{eol}' if FROM_ROW in log_data else ''}"
        f"{ f'Last command direction: {log_data[DIRECTION]}{eol}' if DIRECTION in log_data else ''}"
    )
    return parsed_data


def add_board_if_not_data(data):
    parsed_data = str()
    if "board" in data:

        parsed_data += "Board as seen by not-active player:" + "\n" + "\n"
        row = ''
        for count, char in enumerate(data["board"]):
            row += char
            if (count + 1) % ROW_SIZE == 0:
                parsed_data += row + "\n"
                row = ''
        parsed_data += "\n\n"
    return parsed_data


def generate_text(all_data):

    logs_as_string_list = list()
    for index, data in enumerate(all_data):
        if "data" in all_data[index]:
            logs_as_string_list.append(add_text_if_data(all_data[index]))
        else:
            logs_as_string_list.append(
                add_text_if_not_data(data) + add_board_if_not_data(data)
            )

    return logs_as_string_list


def generate_text_str(data):
    myStr = "Document start\n\n" + ''.join(generate_text(data))
    return myStr
