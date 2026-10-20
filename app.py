
import os
import streamlit as st
from groq import Groq

# ---------------------------------------
# RIO - AI CHEMISTRY TUTOR
# Class 10 | English + Roman Urdu
# ---------------------------------------

st.set_page_config(
    page_title="RIO Chemistry Tutor",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 RIO — AI Chemistry Tutor")
st.subheader("Your Personal Class 10 Chemistry Assistant")

st.markdown(
    """
    Learn Chemistry with AI!

    - 📘 Definitions and explanations
    - 🌍 English and Roman Urdu
    - 🧪 Chemistry examples and equations
    - 📊 Simple labelled text diagrams
    - ✍️ Practice questions
    """
)

SYSTEM_PROMPT = """
You are RIO, a friendly AI Chemistry Tutor for Class 10 students.

Explain chemistry topics in BOTH English and Roman Urdu.

For each new topic, include:
1. Topic name
2. Definition in English
3. Definition in Roman Urdu
4. Detailed explanation in simple language
5. Explanation in Roman Urdu
6. Important points
7. Daily-life examples
8. Chemistry examples
9. Relevant chemical equations, balanced correctly
10. Simple labelled text diagrams where useful
11. Important terms and meanings
12. Three practice questions
13. A short summary

Use text diagrams inside code blocks. Clearly label diagram parts
and explain what each diagram represents. Do not claim a text
diagram is an actual image.

Teach at Class 10 level. Explain formulas and calculations step
by step. Be scientifically accurate. If a student asks a follow-up,
answer it directly. Ask for clarification if a topic is unclear.
"""

# Read API key from Streamlit secrets or environment variable
try:
    api_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    api_key = ""

api_key = api_key or os.getenv("GROQ_API_KEY", "")

# You can change the model using Streamlit secrets
try:
    model_name = st.secrets.get(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )
except Exception:
    model_name = "openai/gpt-oss-20b"

if not api_key:
    st.info(
        "To start RIO, add your Groq API key in "
        "Streamlit Cloud → App settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)

# Start or restore conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chemistry topic input
prompt = st.chat_input(
    "Enter a Chemistry topic, e.g. Atomic Structure..."
)

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("RIO is preparing your lesson..."):
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        *st.session_state.messages
                    ],
                    temperature=0.4,
                    max_completion_tokens=3000
                )

                answer = response.choices[0].message.content

                if not answer:
                    answer = "RIO could not generate an answer. Please try again."

                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(
                "RIO could not generate a response. "
                "Check your API key, model access, internet "
                "connection, and Groq usage limits."
            )
            st.caption(f"Technical details: {e}")

# Sidebar
with st.sidebar:
    st.header("🧪 About RIO")
    st.write("Your AI-powered Chemistry learning assistant.")
    st.write("**Level:** Class 10")
    st.write("**Languages:** English + Roman Urdu")
    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Python, Streamlit and Groq API.")
