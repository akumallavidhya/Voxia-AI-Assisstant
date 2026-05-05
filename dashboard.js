let recognition;
let isListening = false;

/* ---------------- SEND MESSAGE ---------------- */

async function sendMessage(){

let input = document.getElementById("textInput")
let message = input.value.trim()

if(message === "") return

// 🔴 prevent duplicate sends
if(input.disabled) return
input.disabled = true

let chatBox = document.getElementById("chatBox")

let user = document.createElement("div")
user.className = "user-message"
user.innerText = message
chatBox.appendChild(user)

try{

const response = await fetch("/ask",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:message
})
})

const data = await response.json()

let bot = document.createElement("div")
bot.className="bot-message"
bot.innerText=data.reply
chatBox.appendChild(bot)

let history=document.getElementById("historyList")
let item=document.createElement("li")
item.innerText=message
history.appendChild(item)

}catch(err){
console.log("Error:", err)
}

input.value=""
input.disabled = false

chatBox.scrollTop=chatBox.scrollHeight
}


/* ---------------- VOICE RECOGNITION ---------------- */

function startVoice(){

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

if(!SpeechRecognition){
alert("Voice recognition not supported in this browser")
return
}

// prevent multiple starts
if(isListening) return

recognition = new SpeechRecognition()

recognition.lang = "en-IN"
recognition.continuous = false        // ✅ FIXED
recognition.interimResults = false    // ✅ FIXED

recognition.start()

isListening = true

document.getElementById("voiceStatus").innerText = "🎤 Listening..."
console.log("Mic started")

recognition.onresult = function(event){

let transcript = event.results[0][0].transcript.trim()

if(transcript !== ""){

console.log("Voice detected:", transcript)

// show in input
document.getElementById("textInput").value = transcript

// stop BEFORE sending
recognition.stop()
isListening = false

sendMessage()
}

}

recognition.onerror = function(event){
console.log("Mic error:", event.error)
document.getElementById("voiceStatus").innerText = "❌ Mic error"
}

recognition.onend = function(){
isListening = false
document.getElementById("voiceStatus").innerText = "Voice: Stopped"
console.log("Mic stopped")
}

}


/* ---------------- STOP VOICE ---------------- */

function stopVoice(){

if(recognition && isListening){
recognition.stop()
isListening = false

document.getElementById("voiceStatus").innerText = "🛑 Voice stopped"
console.log("Stopped manually")
}

}