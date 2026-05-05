function sendMessage(){

let input = document.getElementById("textInput").value

let chat = document.getElementById("chatBox")

let message = document.createElement("div")

message.innerHTML = "<b>You:</b> " + input

chat.appendChild(message)

let history = document.getElementById("historyList")

let item = document.createElement("li")

item.innerText = input

history.appendChild(item)

document.getElementById("textInput").value = ""

}


function startVoice(){
alert("Voice recognition will start here")
}

function stopVoice(){
alert("Voice stopped")
}