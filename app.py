import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os

LOG_FILE = "log.csv"

# 사용자 설정
user_dict = {
    "SR01": "SR01",
    "SR02": "SR02",
    "SR03": "SR03",
    "SR04": "SR04",
    "SR05": "SR05",
    "SR06": "SR06",
    "SR07": "SR07",
    "SR08": "SR08",
    "SR09": "SR09",
    "SR10": "SR10",
    "SR11": "SR11",
    "SR12": "SR12",
    "SR13": "SR13",
    "admin": "admin"
}

# 한국 시간(KST) 설정 함수
def get_kst_now():
    return datetime.utcnow() + timedelta(hours=9)

# 초기 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.start_time = None

# 로그인
if not st.session_state.logged_in:
    st.title("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if username in user_dict and user_dict[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

else:
    st.success(f"{st.session_state.username}님 환영합니다.")
    
    # 관리자 페이지
    if st.session_state.username == "admin":
        st.header("📊 관리자 페이지: 제출 기록")
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            st.dataframe(df)
            st.download_button("엑셀로 다운로드", df.to_csv(index=False).encode("utf-8"), file_name="제출기록.csv")
        else:
            st.info("제출 기록이 아직 없습니다.")
    else:
        # 사용자 제출 인터페이스
        st.header("✅ 기존 수기 방식")

        if st.session_state.start_time is None:
            if st.button("식단 설계 시작"):
                st.session_state.start_time = get_kst_now()
                st.success(f"시작 시간: {st.session_state.start_time.strftime('%H:%M:%S')}")

        uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx", "xls"])

        if uploaded_file and st.button("📤 제출하기"):
            if st.session_state.start_time:
                submit_time = get_kst_now()
                duration = (submit_time - st.session_state.start_time).total_seconds()
                
                # 기록 저장
                log_data = pd.DataFrame([{
                    "사용자": st.session_state.username,
                    "시작시간": st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "제출시간": submit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "소요시간(초)": int(duration)
                }])

                # 기존 파일 있으면 추가, 없으면 새로 생성
                if os.path.exists(LOG_FILE):
                    existing = pd.read_csv(LOG_FILE)
                    log_data = pd.concat([existing, log_data], ignore_index=True)
                log_data.to_csv(LOG_FILE, index=False)

                st.success("제출 완료되었습니다!")
                st.dataframe(log_data)

                # 초기화
                st.session_state.start_time = None
            else:
                st.warning("먼저 설계 시작 버튼을 눌러주세요.")
