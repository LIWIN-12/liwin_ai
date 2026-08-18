/* =========================================================
   LIWIN AI
   Clean Chat Interface
========================================================= */

const API = "/chat";
const SESSION_KEY = "liwin_ai_session_id";

/* =========================================================
   SESSION
========================================================= */

let SESSION_ID = localStorage.getItem(SESSION_KEY);

if (!SESSION_ID) {
    SESSION_ID = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, SESSION_ID);
}


/* =========================================================
   DOM ELEMENTS
========================================================= */

const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");


/* =========================================================
   INITIALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* New conversation button */
    if (newChatBtn) {
        newChatBtn.addEventListener("click", newConversation);
    }

    /* Send button */
    if (sendBtn) {
        sendBtn.addEventListener("click", send);
    }

    /* Enter = send
       Shift + Enter = new line */
    if (messageInput) {
        messageInput.addEventListener("keydown", (event) => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {
                event.preventDefault();
                send();
            }
        });
    }

    /* First welcome message */
    showWelcomeMessage();

    /* Focus input */
    if (messageInput) {
        messageInput.focus();
    }
});


/* =========================================================
   TIME
========================================================= */

function getTime() {

    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


/* =========================================================
   FORMAT AI RESPONSE
========================================================= */

function formatAIResponse(text) {

    if (!text) {
        return "";
    }

    let formatted = escapeHTML(text);

    /*
     * Basic markdown support
     */

    /* Bold */
    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    /* Inline code */
    formatted = formatted.replace(
        /`([^`]+)`/g,
        "<code>$1</code>"
    );

    /* Bullet points */
    formatted = formatted.replace(
        /^\s*[-•]\s+(.+)$/gm,
        "• $1"
    );

    /* New lines */
    formatted = formatted.replace(
        /\n/g,
        "<br>"
    );

    return formatted;
}


/* =========================================================
   ADD USER MESSAGE
========================================================= */

function addUserMessage(text) {

    const div = document.createElement("div");

    div.className = "user";

    div.innerHTML = `
        <span>YOU</span>
        <small>${getTime()}</small>
        <div class="message-content">
            ${escapeHTML(text)}
        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();
}


/* =========================================================
   ADD AI MESSAGE
========================================================= */

function addAIMessage(text) {

    const div = document.createElement("div");

    div.className = "ai";

    div.innerHTML = `
        <span>LIWIN AI</span>
        <small>${getTime()}</small>
        <div class="message-content">
            ${formatAIResponse(text)}
        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();
}


/* =========================================================
   THINKING INDICATOR
========================================================= */

function showThinking() {

    removeThinking();

    const div = document.createElement("div");

    div.className = "ai thinking-message";

    div.id = "thinking";

    div.innerHTML = `
        <span>LIWIN AI</span>
        <div class="thinking">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();
}


function removeThinking() {

    const thinking = document.getElementById("thinking");

    if (thinking) {
        thinking.remove();
    }
}


/* =========================================================
   ERROR MESSAGE
========================================================= */

function showError(message) {

    const div = document.createElement("div");

    div.className = "system error-message";

    div.innerHTML = `
        <span>LIWIN AI</span>
        <div class="message-content">
            ${escapeHTML(message)}
        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();
}


/* =========================================================
   WELCOME MESSAGE
========================================================= */

function showWelcomeMessage() {

    if (!chatBox) {
        return;
    }

    chatBox.innerHTML = "";

    addAIMessage(
        "Hi! I'm Liwin AI. Ask me about my projects, skills, experience, or career."
    );
}


/* =========================================================
   SCROLL
========================================================= */

function scrollToBottom() {

    if (!chatBox) {
        return;
    }

    requestAnimationFrame(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}


/* =========================================================
   SET INPUT STATE
========================================================= */

function setInputState(disabled) {

    if (messageInput) {
        messageInput.disabled = disabled;
    }

    if (sendBtn) {
        sendBtn.disabled = disabled;
    }

    if (disabled) {

        sendBtn.style.opacity = "0.6";
        sendBtn.style.cursor = "not-allowed";

    } else {

        sendBtn.style.opacity = "";
        sendBtn.style.cursor = "";

    }
}


/* =========================================================
   SEND MESSAGE
========================================================= */

async function send() {

    if (!messageInput) {
        return;
    }

    const question = messageInput.value.trim();

    /* Don't send empty messages */
    if (!question) {
        return;
    }

    /* Prevent multiple requests */
    if (sendBtn && sendBtn.disabled) {
        return;
    }


    /* Show user message */

    addUserMessage(question);


    /* Clear input */

    messageInput.value = "";


    /* Disable input */

    setInputState(true);


    /* Show thinking */

    showThinking();


    try {

        const response = await fetch(API, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                session_id: SESSION_ID
            })

        });


        /* Handle HTTP errors */

        if (!response.ok) {

            let errorMessage =
                "Something went wrong while contacting Liwin AI.";

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage = errorData.detail;
                }

            } catch {
                /* Ignore invalid error response */
            }

            throw new Error(errorMessage);
        }


        /* Parse response */

        const data = await response.json();


        /* Remove thinking */

        removeThinking();


        /* Validate AI response */

        if (
            !data ||
            typeof data.answer !== "string" ||
            !data.answer.trim()
        ) {

            throw new Error(
                "Liwin AI returned an empty response."
            );
        }


        /* Show AI answer */

        addAIMessage(data.answer);

    }


    catch (error) {

        console.error(
            "Liwin AI request failed:",
            error
        );


        removeThinking();


        showError(
            error.message ||
            "Unable to connect to Liwin AI. Please try again."
        );

    }


    finally {

        setInputState(false);

        messageInput.focus();

    }
}


/* =========================================================
   NEW CONVERSATION
========================================================= */

function newConversation() {

    /*
     * Generate a completely new session ID.
     * This separates the new conversation from
     * the previous memory session.
     */

    SESSION_ID = crypto.randomUUID();

    localStorage.setItem(
        SESSION_KEY,
        SESSION_ID
    );


    /* Remove old messages */

    if (chatBox) {
        chatBox.innerHTML = "";
    }


    /* Clear input */

    if (messageInput) {
        messageInput.value = "";
    }


    /* Reset input */

    setInputState(false);


    /* Welcome message */

    showWelcomeMessage();


    /* Focus */

    if (messageInput) {
        messageInput.focus();
    }
}


/* =========================================================
   OPTIONAL: CTRL/CMD + ENTER
========================================================= */

if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        (event) => {

            if (
                (event.ctrlKey || event.metaKey) &&
                event.key === "Enter"
            ) {

                event.preventDefault();

                send();
            }
        }
    );
}