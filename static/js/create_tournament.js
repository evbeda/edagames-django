var list = [];
var listArray = [];

function copyValue() {
    var srcList = document.getElementById("bots");
    var dstList = document.getElementById("clonedBots");
    var clonedIndex = srcList.selectedIndex;
    var botsList = document.getElementById("id_bots_selected")
    // -1 means list is empty
    if (clonedIndex !== -1) {
      var selectedBot = srcList[srcList.selectedIndex];
      dstList.appendChild(selectedBot);
      listArray.push(selectedBot.innerText)
    }
    list = dstList.innerText;
    botsList.value = listArray.join(',')
  }
