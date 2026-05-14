import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(page_title="KGC 통합 마케팅 분석", layout="wide")
st.title("📊 정관장 에브리타임 밸런스 실시간 리포트")

# 2. 구글 스프레드시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# [수정] 주소를 가장 깔끔한 형태(ID 중심)로 변경했습니다.
# 뒤의 ?gid=0 같은 부분은 라이브러리가 알아서 처리하도록 뺐습니다.
SHEET_URL = "https://docs.google.com/spreadsheets/d/12G7u0kwszplju89Qkj4MI_0O9X7H2F8u-Tb9DEB6-yY/edit"

def load_data():
    try:
        # 각 시트를 개별적으로 읽어옵니다.
        df_kpi = conn.read(spreadsheet=SHEET_URL, worksheet="KPI", ttl=0)
        df_region = conn.read(spreadsheet=SHEET_URL, worksheet="지역", ttl=0)
        df_age = conn.read(spreadsheet=SHEET_URL, worksheet="연령", ttl=0)
        return df_kpi, df_region, df_age
    except Exception as e:
        # [중요] 에러의 진짜 내용을 화면에 출력합니다. 
        # 이를 통해 권한 문제인지, 시트 이름 문제인지 알 수 있습니다.
        st.error(f"❌ 데이터 로드 중 실제 에러 발생: {e}")
        st.info("💡 팁: 구글 시트 우측 상단 [공유] 버튼에서 서비스 계정 이메일이 '뷰어'로 등록되어 있는지 꼭 확인하세요.")
        st.stop()

# 데이터 불러오기
df_kpi, df_region, df_age = load_data()

# --- 이후 탭 구성 코드는 이전과 동일하게 유지합니다 ---
tab1, tab2, tab3 = st.tabs(["📈 핵심 지표(KPI)", "🗺️ 지역별 성장률", "👥 연령대별 비중"])

with tab1:
    st.subheader("주요 성과 지표")
    k_cols = st.columns(4)
    for i in range(min(len(df_kpi), 4)):
        with k_cols[i]:
            st.metric(label=df_kpi.iloc[i]['label'], value=df_kpi.iloc[i]['value'], delta=df_kpi.iloc[i]['delta'])
    st.divider()
    st.info("🤖 **AI 마케팅 요약**")
    if len(df_kpi) >= 6:
        st.write(df_kpi.iloc[5, 0])

with tab2:
    st.subheader("지역 및 채널별 성장률 분석")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        fig = px.bar(df_region, x="지역", y="성장률", color="지역", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("구매 고객 연령대 분포")
    col_l, col_r = st.columns([1, 1])
    with col_l:
        fig_p = px.pie(df_age, values="비중", names="연령대", hole=0.4)
        st.plotly_chart(fig_p, use_container_width=True)
