
const getLogsFiltered = () => {
    let filteredLogs = [];
    stateOfAction = selectedOption("valid_move")
    kindOfAction = selectedOption("action_kind")
    for (let i = 0; i < listOfLogs.length; i = i+2 ){
        let showLog = true
        if (isNotAll(kindOfAction) &
            listOfLogs[i].action != kindOfAction) {
                showLog = false
        }
        else if (isNotAll(stateOfAction) &
            listOfLogs[i + 1].state != stateOfAction) {
                showLog = false
        }
        if (showLog) {
            filteredLogs.push(textArray[i])
            filteredLogs.push(textArray[i+1])
        }
    }
    download('logs.txt', filteredLogs)
}

const isNotAll = (filter) => {
    return filter != 'all'
}

const selectedOption = (filterId) => {
    let filter = $(`#${filterId}`).get(0);
    return filter.options[filter.selectedIndex].value
}


function download(filename, dataToDownload ) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=unicode,' + encodeURIComponent(dataToDownload));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}


