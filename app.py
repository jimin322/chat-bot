import streamlit as st
import google.generativeai as genai
import pandas as pd

# 운세 데이터
horoscope_data = {
    "양자리": {
        "rank": "3위",
        "fortune": "새로운 시작을 위한 좋은 기운이 가득한 날입니다.",
        "item": "빨간색 액세서리",
        "action": "새로운 도전을 시작해보세요",
        "message": "당신의 용기가 빛나는 날입니다!"
    },
    "황소자리": {
        "rank": "5위",
        "fortune": "안정적이고 차분한 에너지가 돋보이는 하루입니다.",
        "item": "식물",
        "action": "재정 계획을 세워보세요",
        "message": "꾸준함이 행운을 가져올 거예요!"
    },
    "쌍둥이자리": {
        "rank": "2위",
        "fortune": "소통이 활발하게 이루어지는 날입니다.",
        "item": "노트",
        "action": "친구와 대화를 나누세요",
        "message": "당신의 매력이 빛나는 날이에요!"
    },
    "게자리": {
        "rank": "7위",
        "fortune": "감정적인 통찰력이 높아지는 날입니다.",
        "item": "달 모양 장식",
        "action": "일기를 써보세요",
        "message": "내면의 목소리에 귀 기울여보세요."
    },
    "사자자리": {
        "rank": "1위",
        "fortune": "자신감이 넘치고 창의력이 돋보이는 하루입니다.",
        "item": "골드 액세서리",
        "action": "리더십을 발휘해보세요",
        "message": "당신은 오늘의 주인공입니다!"
    },
    "처녀자리": {
        "rank": "6위",
        "fortune": "세세한 것에 대한 직관이 예리해지는 날입니다.",
        "item": "수첩",
        "action": "정리정돈을 해보세요",
        "message": "완벽함 속에 행복이 있어요!"
    },
    "천칭자리": {
        "rank": "4위",
        "fortune": "균형과 조화를 이루는 날입니다.",
        "item": "향수",
        "action": "예술 활동을 해보세요",
        "message": "아름다움을 발견하는 하루가 될 거예요!"
    },
    "전갈자리": {
        "rank": "8위",
        "fortune": "직감이 예리해지는 날입니다.",
        "item": "검은색 옷",
        "action": "명상을 해보세요",
        "message": "신비로운 매력이 당신을 이끌어요!"
    },
    "사수자리": {
        "rank": "9위",
        "fortune": "모험과 탐험의 기운이 감도는 날입니다.",
        "item": "여행 가이드북",
        "action": "새로운 장소를 방문해보세요",
        "message": "자유로운 영혼을 따라가보세요!"
    },
    "염소자리": {
        "rank": "10위",
        "fortune": "책임감과 성실함이 빛나는 날입니다.",
        "item": "시계",
        "action": "목표를 설정해보세요",
        "message": "한 걸음씩 정상에 도달할 거예요!"
    },
    "물병자리": {
        "rank": "11위",
        "fortune": "독창적인 아이디어가 떠오르는 날입니다.",
        "item": "테크 기기",
        "action": "새로운 것을 배워보세요",
        "message": "당신의 독특함이 매력이에요!"
    },
    "물고기자리": {
        "rank": "12위",
        "fortune": "예술적 영감이 넘치는 날입니다.",
        "item": "음악",
        "action": "창작 활동을 해보세요",
        "message": "감성이 물들어가는 하루예요!"
    }
}

# 페이지 설정
st.set_page_config(
    page_title="🔮 오하아사 챗봇",
    page_icon="🔮"
)

# 제목
st.title("🔮 오하아사 챗봇")

# Gemini API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "mode" not in st.session_state:
    st.session_state["mode"] = "일반 챗봇"

# 모드 선택
st.session_state["mode"] = st.radio(
    "모드를 선택하세요",
    ["일반 챗봇", "오하아사 운세"],
    horizontal=True
)

if st.session_state["mode"] == "일반 챗봇":
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

else:  # 오하아사 운세 모드
    st.subheader("🌟 오늘의 별자리 운세")
    
    # 별자리 선택
    selected_sign = st.selectbox(
        "별자리를 선택하세요",
        list(horoscope_data.keys())
    )
    
    if st.button("운세 보기"):
        if selected_sign in horoscope_data:
            data = horoscope_data[selected_sign]
            
            # 개인 운세 표시
            st.markdown(f"### {selected_sign}의 오늘의 운세")
            st.markdown(f"**✨ 오늘의 순위:** {data['rank']}")
            st.markdown(f"**🔮 오늘의 운세:** {data['fortune']}")
            st.markdown(f"**🧷 행운의 아이템:** {data['item']}")
            st.markdown(f"**🚶 추천 행동:** {data['action']}")
            st.markdown(f"**💬 한 줄 응원:** {data['message']}")
            
            # 구분선
            st.markdown("---")
            
            # 전체 별자리 순위 표시
            st.subheader("📊 전체 별자리 순위")
            
            # 데이터프레임 생성
            ranks_data = []
            for sign, info in horoscope_data.items():
                rank_num = int(info['rank'].replace('위', ''))
                ranks_data.append({
                    "별자리": sign,
                    "순위": rank_num,
                    "행운의 아이템": info['item']
                })
            
            df = pd.DataFrame(ranks_data)
            df = df.sort_values('순위')
            
            # 테이블 표시
            st.table(df)
