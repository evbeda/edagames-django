function copyValue() {
    var srcList = document.getElementById("animals");
    var dstList = document.getElementById("clonedAnimals");
    var clonedIndex = srcList.selectedIndex;
    // -1 means list is empty
    if (clonedIndex !== -1) {
      dstList.appendChild(srcList[srcList.selectedIndex]);
    }
  }