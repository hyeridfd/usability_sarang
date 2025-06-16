import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

# ------------------
# 로그인 사용자 정보
# ------------------
user_dict = {
    "user1": "pass1",
    "user2": "pass2",
    "admin": "admin123"  # 관리자 계정
}

# ------------------
# 초기 상태 설정
# ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.start_time = None
    st.session_state.submitted = False
    st.session_state.history_log = []  # 모든 사용자 기록 저장

# ------------------
# 로그인 페이지
# ------------------
st.title("기존 수기 방식 식단 설계 제출 시스템")

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
    username = st.session_state.username
    st.success(f"로그인됨: {username}")

    # ------------------
    # 관리자 페이지
    # ------------------
    if username == "admin":
        st.header("📊 관리자 페이지: 제출 기록 확인")

        if st.session_state.history_log:
            df_log = pd.DataFrame(st.session_state.history_log)
            st.dataframe(df_log)

            # 엑셀 다운로드
            def convert_df_to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='제출기록')
                return output.getvalue()

            excel_data = convert_df_to_excel(df_log)
            st.download_button(
                label="📥 엑셀로 제출기록 다운로드",
                data=excel_data,
                file_name='제출기록.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            st.info("아직 제출된 기록이 없습니다.")

    # ------------------
    # 사용자 페이지
    # ------------------
    else:
        if st.session_state.start_time is None:
            if st.button("✅ 식단 설계 시작"):
                st.session_state.start_time = datetime.now()
                st.success(f"설계 시작 시간: {st.session_state.start_time.strftime('%H:%M:%S')}")

        uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx", "xls"])

        if uploaded_file and st.button("📤 제출하기"):
            if st.session_state.start_time:
                submit_time = datetime.now()
                duration = submit_time - st.session_state.start_time

                # 기록 저장
                record = {
                    "사용자": username,
                    "시작시간": st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "제출시간": submit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "소요시간(초)": int(duration.total_seconds())
                }
                st.session_state.history_log.append(record)

                # 결과 출력
                st.success("제출 완료!")
                st.write(f"**시작 시간:** {record['시작시간']}")
                st.write(f"**제출 시간:** {record['제출시간']}")
                st.write(f"**총 소요 시간:** {duration}")

                st.dataframe(pd.DataFrame([record]))

                # 초기화
                st.session_state.start_time = None
                st.session_state.submitted = True
            else:
                st.warning("먼저 '식단 설계 시작' 버튼을 눌러주세요.")
