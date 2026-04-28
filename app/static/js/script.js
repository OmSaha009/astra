function escapeHtml(t) {
  return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

const i = 0;
let currentStreamingElement = null;

function createMessage(content, type, showSteps = false) {
  const inner = document.getElementById("chatInner");

  if (type == "user") {
    inner.insertAdjacentHTML(
      "beforeend",
      `
        <div class="msg-row user-row" data_message_prompt="${content}">
          <div class="user-bubble">${escapeHtml(content)}</div>
        </div>`,
    );
    MathJax.typesetPromise([inner]);
  } else {
    inner.insertAdjacentHTML(
      "beforeend",
      `
        <div class="msg-row ai-row">
          <div class="ai-header">
            <div class="ai-avatar">
              <svg width="14" height="14" viewBox="0 0 18 18"><path d="M9 2L16 15H2L9 2Z" fill="#000"/></svg>
            </div>
            <span class="ai-label">Astra</span>
          </div>
          <div class="ai-body">${content}</div>
          <div class="action-bar">
          ${
            showSteps
              ? `
            <button class="action-btn steps-btn">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              Generate Steps
            </button>
            `
              : ""
          }
            <button class="action-btn icon-only" title="Copy" onclick="copyResponse(this)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            </button>
            <button class="action-btn icon-only" title="Share" onclick="flashBtn(this,'Shared!')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
            <button class="action-btn icon-only" title="Retry" onclick="flashBtn(this,'Retrying...')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/></svg>
            </button>
            <button class="action-btn icon-only" title="Select" onclick="flashBtn(this,'Selected!')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            </button>
          </div>
        </div>
      <hr class="msg-divider"/>
        
        `,
    );
  }

  return inner;
}

function createEmptyAstraMsg(prompt) {
  const inner = document.getElementById("chatInner");
  inner.insertAdjacentHTML(
    "beforeend",
    `
            <div class="msg-row ai-row">
          <div class="ai-header">
            <div class="ai-avatar">
              <svg width="14" height="14" viewBox="0 0 18 18"><path d="M9 2L16 15H2L9 2Z" fill="#000"/></svg>
            </div>
            <span class="ai-label">Astra</span>
          </div>
          <div class="ai-body"></div>
          <div class="action-bar">
    
            <button class="action-btn icon-only" title="Copy" onclick="copyResponse(this)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            </button>
            <button class="action-btn icon-only" title="Share" onclick="flashBtn(this,'Shared!')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
            <button class="action-btn icon-only" title="Retry" onclick="flashBtn(this,'Retrying...')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/></svg>
            </button>
            <button class="action-btn icon-only" title="Select" onclick="flashBtn(this,'Selected!')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            </button>
          </div>
          <div class="steps-container-${prompt}"></div>
        </div>
      <hr class="msg-divider"/>
  
    `,
  );

  const allMsgs = document.querySelectorAll(".msg-row.ai-row");
  currentStreamingElement = allMsgs[allMsgs.length - 1];

  return currentStreamingElement.querySelector(".ai-body");
}

function renderConversation(msgs) {
  const inner = document.getElementById("chatInner");
  inner.innerHTML = "";
  msgs.forEach((msg, i) => {
    if (msg.role === "user") {
      inner.insertAdjacentHTML(
        "beforeend",
        `
        <div class="msg-row user-row">
          <div class="user-bubble">${escapeHtml(msg.text)}</div>
        </div>`,
      );
    } else {
      inner.insertAdjacentHTML(
        "beforeend",
        `
        <div class="msg-row ai-row">
          <div class="ai-header">
            <div class="ai-avatar">
              <svg width="14" height="14" viewBox="0 0 18 18"><path d="M9 2L16 15H2L9 2Z" fill="#000"/></svg>
            </div>
            <span class="ai-label">Astra</span>
          </div>
          <div class="ai-body">${marked.parse(msg.text)}</div>
          <div class="action-bar">
            <button class="action-btn steps-btn">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              Generate Steps
            </button>
            <button class="action-btn icon-only" title="Copy" onclick="copyResponse(this)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            </button>
            <button class="action-btn icon-only" title="Share" onclick="flashBtn(this,'Shared!')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
            <button class="action-btn icon-only" title="Retry" onclick="flashBtn(this,'Retrying...')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/></svg>
            </button>
            <button class="action-btn icon-only" title="Select" onclick="flashBtn(this,'Selected!')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            </button>
          </div>
        </div>`,
      );
    }
    if (i < msgs.length - 1 && msg.role !== msgs[i + 1]?.role) {
      inner.insertAdjacentHTML("beforeend", '<hr class="msg-divider"/>');
    }
  });
  renderMath();
  document.getElementById("chatArea").scrollTop = 9999;
}

document.getElementById("imageInput").onchange = async (e) => {
  const file = e.target.files[0];
  const fileNameSpan = document.getElementById("imageFileName");

  if (file) {
    fileNameSpan.textContent = `${file.name}`;
    const latex = await ocrOutput(file);

    const previewText = document.getElementById("latex-preview");
    previewText.innerHTML = `$$${latex}$$`;
    MathJax.typesetPromise([previewText]);
    previewText.style.display = "block";

    document.getElementById("messageInput").value += latex;
    
  } else {
    fileNameSpan.textContent = "";
  }
};

// MESSAGE HANDLING
document.getElementById("pdfBtn").onclick = () => {
  document.getElementById("pdfInput").click();
};
document.getElementById("imageBtn").onclick = () => {
  document.getElementById("imageInput").click();
};

const form = document.getElementById("messageForm");
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  let currentSessionId = localStorage.getItem("astra_session_id");
  if (currentSessionId) {
    formData.append("session_id", currentSessionId);
  }

  const subject = document.getElementById("badgeLabel").textContent;
  formData.append("subject", subject);

  const message = formData.get("message");
  if (!message && !formData.get("image") && !formData.get("pdf")) {
    return;
  }

  const imageFile = formData.get("image");
  const hasImage = imageFile && imageFile.size > 0;

  if (hasImage) {
    if (!message) {
      const latex = await ocrOutput(imageFile);
      document.getElementById("messageInput").value = latex;
      formData.set("message", latex);
      formData.delete("image");
    }
  }

  const chatWindow = document.querySelector(".chat-inner");

  const chatArea = document.querySelector(".chat-area");
  if (chatArea.classList.contains("chat-area-centered")) {
    chatArea.classList.remove("chat-area-centered");
  }

  // Create user message container

  createMessage(message, (type = "user"));
  document.getElementById("messageInput").value = "";

  document.getElementById("latex-preview").style.display = "none";
  document.getElementById("messageInput").style.height = '22px';

  // Create loading indicator
  const loader = document.createElement("div");
  loader.classList.add("loader");
  chatWindow.appendChild(loader);

  // Create container for Astra's response
  const astra_content_div = document.createElement("div");
  astra_content_div.classList.add("content");
  const astra_para = document.createElement("p");
  astra_content_div.appendChild(astra_para);

  const astra_parentmsgdiv = document.createElement("div");
  astra_parentmsgdiv.classList.add("assistant", "message");
  chatWindow.setAttribute("data_message_prompt", message);
  astra_parentmsgdiv.innerHTML = `
    <div class="identity">
    <i class="fa-solid fa-meteor gpt user-icon"></i>
    </div>
    `;
  astra_parentmsgdiv.appendChild(astra_content_div);

  const streamingBody = createEmptyAstraMsg(message);

  // Send request to FastAPI backend
  const response = await fetch("/message-response", {
    method: "POST",
    body: formData,
  });

  chatWindow.removeChild(loader);
  chatWindow.appendChild(astra_parentmsgdiv);

  const contentType = response.headers.get("Content-Type");
  const returnedSessionID = response.headers.get("X-session-ID");
  const showSteps = response.headers.get("showSteps");

  if (returnedSessionID) {
    localStorage.setItem("astra_session_id", returnedSessionID);
  }

  if (
    contentType.includes("text/event-stream") ||
    contentType.includes("text/plain")
  ) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullResponse = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);

      fullResponse += chunk;
      streamingBody.innerHTML = fullResponse;
    }
    streamingBody.parentNode.querySelector(".action-bar").insertAdjacentHTML(
      "afterbegin",
      `
                        ${
                          showSteps
                            ? `<button class="action-btn steps-btn">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              Generate Steps
            </button>`
                            : ""
                        }
            `,
    );
    if (window.MathJax && streamingBody) {
      MathJax.typesetPromise([streamingBody])
        .then(() => console.log("Math rendered"))
        .catch((err) => console.log("MathJax error:", err));
    }
  } else {
    try {
      const result = await response.json();
      streamingBody.innerHTML = result.response;

      if (window.MathJax && streamingBody) {
        MathJax.typesetPromise([streamingBody])
          .then(() => console.log("Math rendered"))
          .catch((err) => console.log("MathJax error:", err));
      }
    } catch (e) {
      // If JSON parse fails, treat as stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        fullResponse += chunk;
        streamingBody.parentNode
          .querySelector(".action-bar")
          .insertAdjacentHTML(
            "afterbegin",
            `
                        ${
                          showSteps
                            ? `<button class="action-btn steps-btn">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              Generate Steps
            </button>`
                            : ""
                        }
            `,
          );
      }
      if (window.MathJax && streamingBody) {
        MathJax.typeset([streamingBody])
          .then(() => console.log("Math rendered"))
          .catch((err) => console.log("MathJax error:", err));
      }
    }
  }
});

//Show Steps
document.addEventListener("click", async (e) => {
  if (e.target.classList.contains("steps-btn")) {
    const button = e.target;
    const aiRow = button.closest(".msg-row.ai-row");

    const userRow = aiRow.previousElementSibling;
    const userMessage = userRow.querySelector(".user-bubble").innerText;
    const prompt = userMessage;

    button.disabled = true;
    button.textContent = "Generating...";

    const response = await fetch("/explain-steps", {
      method: "POST",
      body: JSON.stringify({ prompt }),
    });

    const data = await response.json();

    const stepsDiv = document.createElement("div");
    stepsDiv.className = "steps-container";
    aiRow.appendChild(stepsDiv);
    stepsDiv.innerHTML = data.steps;
    if (window.MathJax && stepsDiv) {
      MathJax.typesetPromise([stepsDiv])
        .then(() => console.log("Math rendered"))
        .catch((err) => console.log("MathJax error:", err));
    }
    button.remove();
  }
});
