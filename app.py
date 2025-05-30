import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="🤖 Gemini 챗봇",
    page_icon="🤖"
)

# 제목
st.title("🤖 Gemini 챗봇")

# Gemini API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 채팅 기록 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 채팅 기록 표시
for role, message in st.session_state["chat_history"]:
    with st.chat_message(role):
        st.write(message)

# 사용자 입력 처리
if user_input := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.write(user_input)
    
    # 채팅 기록에 사용자 메시지 추가
    st.session_state["chat_history"].append(("user", user_input))
    
    try:
        # Gemini 응답 생성
        response = model.generate_content(
            user_input,
            stream=False
        )
        
        # Gemini 응답 표시
        with st.chat_message("assistant"):
            st.write(response.text)
        
        # 채팅 기록에 Gemini 응답 추가
        st.session_state["chat_history"].append(("assistant", response.text))
        
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
