import streamlit as st
import requests

st.set_page_config(
    page_title="Liwin AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

/* Hide Streamlit UI */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Background */
.stApp{
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #2563eb 100%
    );
}

/* Title */
.title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#d1d5db;
    margin-bottom:30px;
}

/* Glass Card */

.glass{

background: rgba(255,255,255,0.10);

backdrop-filter: blur(20px);

-webkit-backdrop-filter: blur(20px);

border-radius:25px;

padding:25px;

border:1px solid rgba(255,255,255,.2);

box-shadow:0 8px 32px rgba(0,0,0,.35);

}

/* Chat bubbles */

.user{

background:#2563eb;

color:white;

padding:15px;

border-radius:18px;

margin-top:15px;

margin-left:30%;

}

.ai{

background:rgba(255,255,255,.12);

color:white;

padding:15px;

border-radius:18px;

margin-top:15px;

margin-right:30%;

border:1px solid rgba(255,255,255,.15);

}

/* Input */

textarea{

background:rgba(255,255,255,.15)!important;

color:white!important;

border-radius:15px!important;

}

/* Buttons */

.stButton button{

background:#2563eb;

color:white;

border-radius:12px;

height:50px;

width:100%;

font-size:18px;

border:none;

}

.stButton button:hover{

background:#1d4ed8;

}

</style>
""", unsafe_allow_html=True)

# ---------------- Session ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages=[]

# ---------------- Header ---------------- #

st.markdown("<div class='title'>🤖 Liwin AI</div>",unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Personal AI Portfolio Assistant</div>",unsafe_allow_html=True)

# ---------------- Chat Card ---------------- #

st.markdown("<div class='glass'>",unsafe_allow_html=True)

for msg in st.session_state.messages:

    if msg["role"]=="user":

        st.markdown(
            f"<div class='user'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='ai'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown("</div>",unsafe_allow_html=True)

st.write("")

# ---------------- Input ---------------- #

question=st.chat_input("Ask me about my projects, skills, experience...")

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.spinner("Liwin AI is thinking..."):

        response=requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "question":question
            }
        )

        if response.status_code==200:

            answer=response.json()["answer"]

        else:

            answer="Unable to connect to backend."

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

    st.rerun()