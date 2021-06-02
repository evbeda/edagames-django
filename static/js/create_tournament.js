var innerTextValues = [];
var botObjectsSelected = [];

function copyValue() {
    var srcList = document.getElementById("bots");
    var dstList = document.getElementById("clonedBots");
    var clonedIndex = srcList.selectedIndex;
    var botsList = document.getElementById("id_bots_selected")
    // -1 means list is empty
    if (clonedIndex !== -1) {
      var selectedBot = srcList[srcList.selectedIndex];
      dstList.appendChild(selectedBot);
      botObjectsSelected.push(selectedBot.innerText)
    }
    innerTextValues = dstList.innerText;
    botsList.value = botObjectsSelected.join(',')
  }
