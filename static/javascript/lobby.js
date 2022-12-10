function openChat(){
    var x= document.getElementById("chat-room");
    // console.log(x)
    if(x.style.display=="block"){
        x.style.display="none";
        document.getElementById("popup").style.marginTop="400px";

    }
    else{
       x.style.display="block";
       document.getElementById("popup").style.marginTop="0px";
    }
}