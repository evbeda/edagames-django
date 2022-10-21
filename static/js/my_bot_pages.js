const copyToClickBoard = (data) => {
    navigator.clipboard.writeText(data);
    document.getElementById(data).value ="copied!";
    setTimeout(function(){
      document.getElementById(data).value ="copy";
    }, 2000);
  };

const changeColor = (data) =>{
  document.getElementById(data).style.backgroundColor ="#28a745";
    document.getElementById(data).style.borderColor ="#28a745";
  setTimeout(function(){
    document.getElementById(data).style.backgroundColor ="#4e73df";
    document.getElementById(data).style.borderColor ="#4e73df";
  }, 2000);
}