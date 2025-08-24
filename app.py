import streamlit as st
from gtts import gTTS
from openai import OpenAI
import os

# ---- CONFIG ----
openai_api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenAI API key
client = OpenAI(api_key=openai_api_key)

# ---- STREAMLIT UI ----
st.set_page_config(page_title="AI Avatar Teacher", layout="centered")
st.title("🎓 AI Avatar Teacher (Free Demo)")
st.write("Type your question or paste your work. Get instant feedback with voice and avatar!")

# ---- SESSION STATE FOR CHAT HISTORY ----
if "history" not in st.session_state:
    st.session_state.history = []

# ---- AVATAR OPTIONS ----
avatars = {
    "Friendly Teacher": "https://i.imgur.com/8Km9tLL.png",  # free avatar image
    "Scientist": "https://i.imgur.com/jxWqIBf.png"
}
selected_avatar = st.selectbox("Choose your avatar:", avatars.keys())

# ---- STUDENT INPUT ----
user_input = st.text_area("Your question/answer:")

# ---- GET FEEDBACK ----
if st.button("Get Feedback"):
    if user_input.strip() == "":
        st.warning("Please enter something first.")
    else:
        # System prompt based on avatar
        if selected_avatar == "Scientist":
            system_prompt = "You are a scientist explaining concepts clearly and kindly."
        else:
            system_prompt = "You are a helpful teacher giving constructive feedback."

        # AI response using new OpenAI v1 API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        feedback = response.choices[0].message.content

        # Save in session history
        st.session_state.history.append({"question": user_input, "feedback": feedback})

        # Convert feedback to speech
        tts = gTTS(feedback, lang="en")
        audio_file = "feedback.mp3"
        tts.save(audio_file)

# ---- DISPLAY CHAT HISTORY ----
if st.session_state.history:
    for chat in st.session_state.history[::-1]:  # newest first
        st.markdown("---")
        st.write("**You:**", chat["question"])
        st.write("**AI Feedback:**", chat["feedback"])
        st.audio("feedback.mp3", format="audio/mp3")
        st.image(avatars[selected_avatar], caption="Your AI Teacher")
