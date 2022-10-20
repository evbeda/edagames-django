function copyToClickBoard(data){
    navigator.clipboard.writeText(data);
    document.getElementById(data).value ="copied!"
    setTimeout(function(){
      document.getElementById(data).value ="copy"
    }, 2000);
  };