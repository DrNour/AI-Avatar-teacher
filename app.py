import streamlit as st
from openai import OpenAI
import base64

# Initialize OpenAI client
client = OpenAI()

# Streamlit app title
st.set_page_config(page_title="AI Avatar Teacher", page_icon="🎓", layout="centered")
st.title("🎓 AI Avatar Teacher")

# User input
student_input = st.text_input("✏️ Enter your answer:")

if st.button("Get Feedback"):
    if student_input.strip() == "":
        st.warning("Please enter your answer first.")
    else:
        # Generate feedback using GPT
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a friendly teacher giving constructive feedback."},
                    {"role": "user", "content": student_input}
                ]
            )

            feedback = response.choices[0].message.content
            st.success("✅ Feedback received!")

            # Show teacher avatar
            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                caption="Your AI Teacher",
                width=150
            )

            # Display feedback text
            st.markdown(f"### 📢 Teacher says:\n{feedback}")

            # Convert feedback into speech
            with st.spinner("Generating voice..."):
                speech_response = client.audio.speech.create(
                    model="gpt-4o-mini-tts",
                    voice="alloy",
                    input=feedback
                )

                audio_bytes = speech_response.read()
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

                st.audio(audio_bytes, format="audio/mp3")
