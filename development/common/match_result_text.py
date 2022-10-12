import json

CELL_SIZE = 5
LARGE = 17
ROW_SIZE = LARGE * CELL_SIZE


def add_text_if_data(currentString, data, index):
    newStr = currentString
    newStr += "---------------------------- Player Command -------------------------------------\\n"
    newStr += "Action: " + data[index]["action"] + "\\n"
    innerData = data[index]["data"]
    innerData = json.loads(innerData)
    newStr += "Coordinates: " + str(innerData["from_row"]) + ", " + str(innerData["from_col"]) + "\\n"
    newStr += "Direction: " + innerData["direction"] + "\\n\\n"
    return newStr


def add_text_if_not_data(currentString, myData):
    currentString += "--------------- Resulting Discovered Board after Player Command ------------------\\n"
    currentString += "Player 1 Score: " + myData["score_1"] + "\\n"
    currentString += "Player 2 Score: " + myData["score_2"] + "\\n"
    currentString += "Player 1 Name: " + myData["player_1"] + "\\n"
    currentString += "Player 2 Name: " + myData["player_2"] + "\\n"
    currentString += "Remaining turns: " + myData["remaining_turns"] + "\\n"
    if "from_col" in myData.keys():
        currentString += ("Last command coords: " + myData["from_row"] +
                          ", " + myData["from_col"] + "\\n")
    if "direction" in myData.keys():
        currentString += "Last command direction: " + myData["direction"] + "\\n"
    return currentString


def add_board_if_not_data(currentString, myData):
    currentString += "Board as seen by not-active player:" + "\\n" + "\\n"
    row = ''
    for count, char in enumerate(myData["board"]):
        row += char
        if (count + 1) % ROW_SIZE == 0:
            currentString += row + "\\n"
            row = ''
    currentString += "\\n\\n"
    return currentString


def generate_text(data):
    myStr = "Document start\\n\\n"
    for index, myData in enumerate(data):
        if "data" in data[index].keys():
            myStr = add_text_if_data(myStr, data, index)
        else:
            myStr = add_text_if_not_data(myStr, myData)
            myStr = add_board_if_not_data(myStr, myData)
    return myStr
