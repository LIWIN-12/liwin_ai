// ======================================================
// LIWIN AI OS
// ======================================================
const API = "/chat";
//const API = "http://127.0.0.1:8000/chat";

const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
const clock = document.getElementById("clock");

// ======================================================
// CLOCK
// ======================================================

setInterval(() => {
    const now = new Date();

    clock.innerHTML =
        now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        });

}, 1000);


// ======================================================
// TIMESTAMP
// ======================================================

function time() {

    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });

}


// ======================================================
// TERMINAL MESSAGE
// ======================================================

function addMessage(type, title, text) {

    const div = document.createElement("div");

    div.className = type;

    div.innerHTML = `

        <small>${time()}</small><br><br>

        <span>[${title}]</span>

        <br><br>

        ${text}

    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

}



// ======================================================
// TYPEWRITER
// ======================================================

function typeMessage(text) {

    const div = document.createElement("div");

    div.className = "ai";

    div.innerHTML = `

        <small>${time()}</small><br><br>

        <span>[LIWIN AI]</span>

        <br><br>

        <p class="typing"></p>

    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

    const target = div.querySelector(".typing");

    let i = 0;

    const speed = 10;

    function write() {

        if (i < text.length) {

            target.innerHTML += text.charAt(i);

            i++;

            chatBox.scrollTop = chatBox.scrollHeight;

            setTimeout(write, speed);

        }

    }

    write();

}



// ======================================================
// BOOT SEQUENCE
// ======================================================

window.onload = () => {

    setTimeout(() => {

        addMessage(
            "system",
            "SYSTEM",
            "Initializing Liwin AI Operating System..."
        );

    }, 500);

    setTimeout(() => {

        addMessage(
            "system",
            "SYSTEM",
            "Loading ChromaDB..."
        );

    }, 1500);

    setTimeout(() => {

        addMessage(
            "system",
            "SYSTEM",
            "Connecting Gemini..."
        );

    }, 2500);

    setTimeout(() => {

        addMessage(
            "system",
            "SYSTEM",
            "Knowledge Base Ready."
        );

    }, 3500);

    setTimeout(() => {

        addMessage(
            "ai",
            "LIWIN AI",
            "Hello! I'm Liwin AI. Ask me anything about my experience, projects, skills or career."
        );

    }, 4500);

};




// ======================================================
// SEND
// ======================================================

async function send() {

    const question = messageInput.value.trim();

    if (question === "") return;

    addMessage(

        "user",

        "YOU",

        question

    );

    messageInput.value = "";



    addMessage(

        "system",

        "SYSTEM",

        "Searching Knowledge Base..."

    );



    try {

        const response = await fetch(API, {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                question: question

            })

        });

        const data = await response.json();

        typeMessage(data.answer);

    }

    catch (e) {

        addMessage(

            "system",

            "ERROR",

            "Unable to connect to Liwin AI."

        );

    }

}



// ======================================================

sendBtn.onclick = send;

messageInput.addEventListener("keydown", (e) => {

    if (e.key === "Enter" && !e.shiftKey) {

        e.preventDefault();

        send();

    }

});