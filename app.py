import os
import google.generativeai as genai
import streamlit as st

# ✅ Configure with your Gemini 2.5 Pro API Key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ✅ Use Gemini 2.5 Pro model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config={
        "temperature": 0.8,
        "top_p": 1,
        "max_output_tokens": 2048,
    },
)

# ✅ Start chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ✅ Streamlit UI
st.set_page_config(page_title="Gemini 2.5 Chatbot", layout="centered")
st.title("💬 Gemini 2.5 Pro Chatbot")

user_input = st.text_input("You:", key="input")

if user_input:
    response = st.session_state.chat.send_message(user_input)
    st.markdown(f"**You:** {user_input}")
    st.markdown(f"**Gemini:** {response.text}")

    # Optional: Display full chat history
    st.divider()
    st.subheader("📝 Chat History")
    for turn in st.session_state.chat.history:
        st.markdown(f"**You:** {turn.parts[0].text}")
        st.markdown(f"**Gemini:** {turn.parts[1].text}")
