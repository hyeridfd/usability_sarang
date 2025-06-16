import streamlit as st
from datetime import datetime
import pandas as pd

# ------------------
# 로그인 기능 (간단 버전)
# ------------------
st.title("기존 수기 방식 식단 설계 제출 시스템")

# 로그인 사용자 정보 (실제로는 보안 강화 필요)
user_dict = {
    "user1": "pass1",
    "user2": "pass2"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.start_time = None
    st.session_state.submitted = False

if not st.session_state.logged_in:
    st.subheader("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if username in user_dict and user_dict[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"{username}님 환영합니다!")
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

else:
    st.success(f"로그인됨: {st.session_state.username}")
    
    # ------------------
    # 설계 시작
    # ------------------
    if st.session_state.start_time is None:
        if st.button("✅ 식단 설계 시작"):
            st.session_state.start_time = datetime.now()
            st.success(f"설계 시작 시간: {st.session_state.start_time.strftime('%H:%M:%S')}")

    # ------------------
    # 파일 업로드
    # ------------------
    uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx", "xls"])

    # ------------------
    # 제출 및 시간 측정
    # ------------------
    if uploaded_file and st.button("📤 제출하기"):
        if st.session_state.start_time:
            submit_time = datetime.now()
            duration = submit_time - st.session_state.start_time

            st.success(f"제출 완료!")
            st.write(f"**시작 시간:** {st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**제출 시간:** {submit_time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**총 소요 시간:** {duration}")

            # 결과 기록용 (선택)
            result = pd.DataFrame({
                "사용자": [st.session_state.username],
                "시작시간": [st.session_state.start_time],
                "제출시간": [submit_time],
                "소요시간(초)": [int(duration.total_seconds())]
            })
            st.dataframe(result)

            # 상태 초기화 옵션
            st.session_state.submitted = True
        else:
            st.warning("먼저 '식단 설계 시작' 버튼을 눌러주세요.")
