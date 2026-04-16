const mainView = document.querySelector(".main");
const chatList = document.getElementById("chatList")
const label = chatList.querySelector('.prev-chats-label');
// const item = document.createElement('div');
//     item.className = 'chat-item' + (chat.active ? ' active' : '');
//     item.innerHTML = `
//       <span class="chat-item-text">${chat.title}</span>
//       <button class="chat-item-delete" title="Delete" onclick="deleteChat(event,${chat.id})">
//         <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//           <polyline points="3 6 5 6 21 6"/>
//           <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/>
//           <path d="M10 11v6"/><path d="M14 11v6"/>
//           <path d="M9 6V4h6v2"/>
//         </svg>
//       </button>`;
//     list.appendChild(item);



//New Session
document.getElementById("new-chat-btn").addEventListener("click", async (e) => {

  const response = await fetch("/new-session", {
    method: "POST"
  });
  const {session_id} = await response.json();
  localStorage.setItem("astra_session_id", session_id);
  document.querySelector(".main").innerHTML = "";

});

//LOAD SESSIONS

async function loadSessions() {
  const response = await fetch("/get-sessions");
  const {sessions} = await response.json();
  const chatActive = false;

  chatList.innerHTML += sessions.map(s => 
    `
    <div class="chat-item ${chatActive ? 'active' : ''}" data_session_id="${s.id}">
    
      <span class="chat-item-text">${s.preview || "Untitled Chat"}</span>
      <button class="chat-item-delete" title="Delete">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/>
          <path d="M10 11v6"/><path d="M14 11v6"/>
          <path d="M9 6V4h6v2"/>
        </svg>
      </button>
    
    </div>
    `).join("");

    const chatItemButtons = document.querySelectorAll(".chat-item-text");
    const chatItemDeleteButton = document.querySelectorAll(".chat-item-delete");

    chatItemButtons.forEach(el => {
        el.onclick = () => {
          const sessionID = el.closest(".chat-item").getAttribute("data_session_id")
          loadSessionForID(sessionID);
        };
    });
    chatItemDeleteButton.forEach(el => {
        el.onclick = () => {
          const parentdiv = el.closest(".chat-item")
          const sessionID = parentdiv.getAttribute("data_session_id")
          deleteSessionID(sessionID)
        };
    });
}


async function loadSessionForID(sessionId) {
  const response = await fetch(`/session/${sessionId}/messages`)
  const {messages} = await response.json();
  console.log(messages)

  const chatWindow = document.querySelector(".chat-inner");

  const chatArea = document.querySelector(".chat-area");
  if (chatArea.classList.contains("chat-area-centered")){chatArea.classList.remove("chat-area-centered")};

  console.log(chatWindow);
  chatWindow.innerHTML = "";

  for(let i=0; i < messages.length ; i+=2){
    const userMsg = messages[i];
    const astraMsg = messages[i+1];
    console.log(userMsg, astraMsg);

    if(userMsg && userMsg.role == "user"){
      const msgdiv = createMessage(userMsg.content, "user")
      console.log(msgdiv)
    }

    if(astraMsg && astraMsg.role == "astra"){
      const msgdiv = createMessage(astraMsg.content, "astra")
      console.log(msgdiv)
    }

  }
  localStorage.setItem("astra_session_id", sessionId);
  if (window.MathJax) {
        MathJax.typesetPromise([chatWindow])
          .then(() => console.log("Math rendered"))
          .catch((err) => console.log("MathJax error:", err));
  }
}


async function deleteSessionID(sessionID) {
  console.log("DELETING SESSION: ", sessionID)
  const response =  await fetch(`/session/${sessionID}/delete`);
  const code = await response.json()
  console.log("DELETED")
  document.querySelector(`div  [data_session_id="${sessionID}"]`).remove()
}



loadSessions();

