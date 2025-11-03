import streamlit as st
import difflib
from gtts import gTTS
import tempfile
import speech_recognition as sr
import os

st.title("🎧 AI 영어 발음 교정기")

# 1️⃣ 단어 입력
word = st.text_input("연습할 단어를 입력하세요:")

if word:
    st.write(f"연습 단어: **{word}**")

    # 2️⃣ 원어민 발음 재생
    tts = gTTS(word, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name, format="audio/mp3")

    # 3️⃣ 사용자 발음 녹음
    st.write("🎙️ 발음을 녹음한 후, 파일을 업로드하세요 (예: myvoice.wav)")
    uploaded_file = st.file_uploader("녹음 파일 업로드", type=["wav", "mp3"])

    if uploaded_file:
        # 4️⃣ 음성 인식
        recognizer = sr.Recognizer()
        with sr.AudioFile(uploaded_file) as source:
            audio_data = recognizer.record(source)
            try:
                result = recognizer.recognize_google(audio_data)
                st.write(f"🗣️ 인식 결과: **{result}**")

                # 5️⃣ 점수 계산
                similarity = difflib.SequenceMatcher(None, word.lower(), result.lower()).ratio()
                score = round(similarity * 100, 1)
                st.write(f"📊 발음 점수: **{score}점**")

                # 6️⃣ 피드백
                if score == 100:
                    st.success("완벽해요! 원어민 수준이에요! 💯")
                elif score >= 80:
                    st.info("좋아요! 약간의 발음 개선만 필요해요 👌")
                else:
                    st.warning("조금 더 연습해볼까요? 특히 모음이나 강세를 주의해보세요 😅")

            except sr.UnknownValueError:
                st.error("음성을 인식하지 못했어요. 다시 시도해주세요!")
