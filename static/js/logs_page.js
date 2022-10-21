let listOfLogs = [];
let index = 0;
const KEYSUSER = ["action","direction","from_col","from_row","game_id","turn_token"];
const KEYSUSERTIMEOUT = ["event","player"];
const SERVERKEY = [
    "state",
    "remaining_turns", 
    "arrows_1",
    "arrows_2",   
    "direction",
    "from_col",
    "from_row",
    "player_1",
    "player_2",
    "score_1",
    "score_2",
    "side",
    "game_id", 
    "board",
]
const CELL_SIZE = 5
const LARGE = 17
const ROW_SIZE = LARGE * CELL_SIZE
const keyAction = "action";
const keyBoard = "board";
const keyData = "data";
const keyEvent = "event";
const keyPlayer = "player";
const CHARACTERPERCELL = /.{1,5}/g;
const replaceQuotationMarks = [[`'`,`"`],[`"{`,"{"],[`}"`,"}"]]


const addLogToArray = (log) =>{   
    replaceQuotationMarks.forEach((replace)=>{
        log = log.replaceAll(replace[0],replace[1])
    })
    listOfLogs.push(JSON.parse(log))
}

const modifiDOMElementUser = (key, log = null) =>{
    if(key == keyAction || key == keyEvent || key == keyPlayer ){
        document.getElementById(key).innerHTML =  (log && listOfLogs[index][key])  ? listOfLogs[index][key] : "";
    }else{
        document.getElementById(key).innerHTML = log  ? listOfLogs[index][keyData][key] : "";
    }
}

const modifiDOMElementServer = (key,log = null) =>{
    if (key == keyBoard){
        listOfLogs[index][key] && beatiBoard(listOfLogs[index][key]);
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
    let array_board = board.match(CHARACTERPERCELL);
    const boardToHTML = document.getElementById("containerBoard");
    boardToHTML.textContent = '';
    for (let rows = 0; rows <= (LARGE - 1); rows++) {
        let rowHTML = document.createElement("span");
        rowHTML.classList.add("rowContainer");
        for (let columns = 0; columns <= (LARGE - 1); columns++) {
            let columnHTML = document.createElement("span");
            columnHTML.classList.add("spaces");
            let textHTML = document.createTextNode(array_board[(rows*LARGE)+columns]);
            columnHTML.appendChild(textHTML);
            rowHTML.appendChild(columnHTML);
        }
        boardToHTML.appendChild(rowHTML);
    }
}

//export function add variables to test
// Like a object 
if(typeof window == "undefined"){
    module.exports = {
        addLogToArray: addLogToArray,
        listOfLogs:listOfLogs,
        updateDomElement:updateDomElement
    };
}