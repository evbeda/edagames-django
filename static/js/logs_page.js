let listOfLogs = [];
let index = 0;
const KEYSUSER = ["action","direction","from_col","from_row","game_id","turn_token"];
const KEYSUSERTIMEOUT = ["event","player"];
const SERVERKEY = [
    "score_2", 
    "remaining_turns", 
    "arrows_2", 
    "side", 
    "player_1", 
    "score_1",
    "from_col",
    "score_1",
    "from_col",
    "direction",
    "game_id",
    "board",
    "player_2",
    "arrows_1",
    "from_row",
    "state",
    "current_player"
]
const CELL_SIZE = 5
const LARGE = 17
const ROW_SIZE = LARGE * CELL_SIZE
const keyAction = "action";
const keyBoard = "board";
const keyData = "data";
const keyEvent = "event";
const keyPlayer = "player";


const addLogToArray = (log) =>{
    listOfLogs.push(log)
}

const modifiDOMElementUser = (key, log = null) =>{
    switch (key) {
        case keyAction:
            document.getElementById(key).innerHTML =  log  ? listOfLogs[index][key] : "";
            break;
        case keyPlayer:
            document.getElementById(key).innerHTML =  (log && listOfLogs[index][key])  ? listOfLogs[index][key] : "";
            break;
        case keyEvent:
            document.getElementById(key).innerHTML =  (log && listOfLogs[index][key])  ? listOfLogs[index][key] : "";
            break;
        default:
            document.getElementById(key).innerHTML = log  ? listOfLogs[index][keyData][key] : "";
            break;
    }
}

const modifiDOMElementServer = (key,log = null) =>{
    if (key == keyBoard && listOfLogs[index][key]){
        beatiBoard(listOfLogs[index][key] || " ");
    }else{
        document.getElementById("server_"+key).innerHTML =  (log && listOfLogs[index][key])  ? listOfLogs[index][key] : "";
    }
}

const firstView = () =>{
    if (index == 0){
        updateDomElement();
    }
} 

const updateDomElement = () =>{
    let updateUserTimeOut = false;
    let updateUserAction = false;
    let updateServer = false;
    if(listOfLogs[index].hasOwnProperty(keyData)){
        updateUserAction = true;
    }else if(listOfLogs[index].hasOwnProperty(keyEvent)){
        updateUserTimeOut = true;
    }else{
        updateServer = true;
    }

    KEYSUSERTIMEOUT.forEach(key => {
        modifiDOMElementUser(key,updateUserTimeOut)
    });
    KEYSUSER.forEach(key => {
        modifiDOMElementUser(key,updateUserAction)
    });
    SERVERKEY.forEach(key =>{
        modifiDOMElementServer(key,updateServer)
    });

}

const modifyIndex = (operation) => {
    if(operation == "+" && index < listOfLogs.length){
        index ++;
        updateDomElement();
    }
    if(operation == "-" && index > 0){
        index --;
        updateDomElement();
    }
}

const beatiBoard = (board) =>{
    let row_index = 16;
    let colunm_index = 16;
    let array_board = board.match(/.{1,5}/g);
    for (let rows = 0; rows <= row_index; rows++) {
        for (let columns = 0; columns <= colunm_index; columns++) {
            document.getElementById("row_"+rows+"_col_"+columns).innerHTML = array_board[(rows*17)+columns];
        }
    }
    // board.split('').forEach((char, index) => {
    //     row += char === " " ? char.replace(" ", "_") : char
    //     if((index + 1) % ROW_SIZE == 0){
    //         document.getElementById("row_"+spanIndex).innerHTML = row;
    //         spanIndex++;
    //         row =""
    //     }
    // });
    //return currentString
}



