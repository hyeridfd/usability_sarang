import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os

# 페이지 설정
st.set_page_config(
    page_title=" 기존 수기 방식 식단 개선 시스템",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS
st.markdown("""
<style>
    /* 메인 배경 */
    .main {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* 카드 스타일 컨테이너 */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* 로그인 카드 */
    .login-card {
        max-width: 400px;
        margin: 5rem auto;
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* 제목 스타일 */
    .title {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .subtitle {
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* 성공 메시지 스타일 */
    .success-banner {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    /* 관리자 헤더 */
    .admin-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 사용자 헤더 */
    .user-header {
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 위험 버튼 */
    .danger-button button {
        background: linear-gradient(45deg, #ff416c, #ff4b2b) !important;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3) !important;
    }
    
    .danger-button button:hover {
        box-shadow: 0 6px 20px rgba(255, 65, 108, 0.4) !important;
    }
    
    /* 시작 버튼 */
    .start-button button {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf) !important;
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.3) !important;
        font-size: 1.1rem !important;
        padding: 1rem 2.5rem !important;
    }
    
    /* 파일 업로더 스타일 */
    .stFileUploader {
        background: #f8f9fa;
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
    
    /* 데이터프레임 스타일 */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 통계 카드 */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
    }
</style>
""", unsafe_allow_html=True)

LOG_FILE = "log.csv"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

def get_kst_now():
    return datetime.utcnow() + timedelta(hours=9)

# 초기 상태
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.start_time = None

# 로그인 화면
if not st.session_state.logged_in:
    # 빈 공간으로 상단 여백 생성
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 로그인 카드
    st.markdown("""
    <div class="login-card">
        <h1 style="color: #667eea; margin-bottom: 0.5rem;">🍽️</h1>
        <h2 style="color: #2c3e50; margin-bottom: 0.5rem;">식단 설계 시스템</h2>
        <p style="color: #7f8c8d; margin-bottom: 2rem;">로그인하여 시작하세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 로그인 폼을 카드 안에 배치
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 아이디", placeholder="아이디를 입력하세요")
            password = st.text_input("🔒 비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            
            if st.button("🚀 로그인", use_container_width=True):
                if username in user_dict and user_dict[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")

else:
    # 환영 메시지
    st.markdown(f"""
    <div class="success-banner">
        🎉 {st.session_state.username}님 환영합니다!
    </div>
    """, unsafe_allow_html=True)

    # 🔒 관리자 페이지
    if st.session_state.username == "admin":
        st.markdown("""
        <div class="admin-header">
            <h1>🔧 관리자 페이지</h1>
            <p>시스템 관리 및 제출 기록 확인</p>
        </div>
        """, unsafe_allow_html=True)

        # 통계 카드들
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(df)}</div>
                    <div class="stat-label">총 제출 수</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{df['사용자'].nunique()}</div>
                    <div class="stat-label">참여 사용자</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_time = int(df['소요시간(초)'].mean()) if '소요시간(초)' in df.columns else 0
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{avg_time}초</div>
                    <div class="stat-label">평균 소요시간</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                today_count = len(df[df['제출시간'].str.contains(datetime.now().strftime('%Y-%m-%d'))])
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{today_count}</div>
                    <div class="stat-label">오늘 제출</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 관리 버튼들
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.markdown('<div class="danger-button">', unsafe_allow_html=True)
            if st.button("🗑️ 기록 전체 삭제", use_container_width=True):
                if os.path.exists(LOG_FILE):
                    os.remove(LOG_FILE)
                    st.success("✅ 로그 파일이 삭제되었습니다.")
                else:
                    st.warning("⚠️ 삭제할 로그 파일이 없습니다.")
            st.markdown('</div>', unsafe_allow_html=True)

        # 제출 기록 테이블
        st.markdown("""
        <div class="card">
            <h3>📊 제출 기록</h3>
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            st.dataframe(df, use_container_width=True)

            # 사용자 선택 및 파일 다운로드
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                user_list = df["사용자"].unique().tolist()
                selected_user = st.selectbox("👤 사용자 선택", user_list)
            
            with col2:
                user_file = os.path.join(UPLOAD_FOLDER, f"{selected_user}_제출파일.xlsx")
                if os.path.exists(user_file):
                    with open(user_file, "rb") as f:
                        st.download_button(
                            label=f"📥 {selected_user} 제출 파일 다운로드",
                            data=f,
                            file_name=f"{selected_user}_제출파일.xlsx",
                            use_container_width=True
                        )
                else:
                    st.warning(f"⚠️ {selected_user}님의 제출 파일이 존재하지 않습니다.")
        else:
            st.info("📝 제출 기록이 아직 없습니다.")

    # 🙋 사용자 페이지
    else:
        # 시작 버튼 섹션
        st.markdown("""
        <div class="card">
            <h3>🚀 작업 시작</h3>
            <p>아래 버튼을 클릭하여 기존 방식으로 식단 개선 작업을 시작하세요.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.start_time is None:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown('<div class="start-button">', unsafe_allow_html=True)
                if st.button("🍽️ 식단 설계 시작", use_container_width=True):
                    st.session_state.start_time = get_kst_now()
                    st.success(f"⏰ 시작 시간: {st.session_state.start_time.strftime('%H:%M:%S')}")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
             with col2:   
                 if st.button("🚪 로그아웃", use_container_width=True):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.start_time = None
                    st.rerun()

        else:
            # 진행 중 상태 표시
            current_time = get_kst_now()
            elapsed = current_time - st.session_state.start_time
            elapsed_seconds = int(elapsed.total_seconds())
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #56ab2f, #a8e6cf); color: white; 
                        padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
                ⏱️ 작업 진행 중... | 시작 시간: {st.session_state.start_time.strftime('%H:%M:%S')} 
                | 경과 시간: {elapsed_seconds}초
            </div>
            """, unsafe_allow_html=True)

        # 파일 업로드 섹션
        if st.session_state.start_time:
            st.markdown("""
            <div class="card">
                <h3>📁 파일 업로드</h3>
                <p>완성된 식단 설계 엑셀 파일을 업로드해주세요.</p>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "📊 엑셀 파일 선택", 
                type=["xlsx", "xls"],
                help="xlsx 또는 xls 파일만 업로드 가능합니다."
            )

            if uploaded_file:
                st.success(f"✅ 파일 선택됨: {uploaded_file.name}")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("📤 제출하기", use_container_width=True):
                        submit_time = get_kst_now()
                        duration = (submit_time - st.session_state.start_time).total_seconds()

                        file_path = os.path.join(UPLOAD_FOLDER, f"{st.session_state.username}_제출파일.xlsx")
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        log_data = pd.DataFrame([{
                            "사용자": st.session_state.username,
                            "시작시간": st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "제출시간": submit_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "소요시간(초)": int(duration),
                            "파일경로": file_path
                        }])

                        if os.path.exists(LOG_FILE):
                            existing = pd.read_csv(LOG_FILE)
                            # 파일경로 컬럼이 없으면 추가
                            if '파일경로' not in existing.columns:
                                existing['파일경로'] = None
                            log_data = pd.concat([existing, log_data], ignore_index=True)

                        log_data.to_csv(LOG_FILE, index=False)

                        
                        st.success("🎉 제출이 완료되었습니다!")
                        
                        # 결과 요약
                        st.markdown(f"""
                        <div style="background: #e8f5e8; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                            <h4>📋 제출 완료 요약</h4>
                            <p><strong>👤 사용자:</strong> {st.session_state.username}</p>
                            <p><strong>⏰ 소요 시간:</strong> {int(duration)}초</p>
                            <p><strong>📅 제출 시간:</strong> {submit_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.start_time = None
