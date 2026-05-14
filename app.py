import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(page_title="KGC 통합 마케팅 분석", layout="wide")
st.title("📊 정관장 에브리타임 밸런스 실시간 리포트")

# 2. 구글 스프레드시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)
# 본인의 실제 스프레드시트 URL을 따옴표 안에 넣으세요.
SHEET_URL = "https://docs.google.com/spreadsheets/d/12G7u0kwszplju89Qkj4MI_0O9X7H2F8u-Tb9DEB6-yY"

# 데이터를 안전하게 로드하기 위한 함수
def load_data():
    try:
        # 시트 이름(worksheet)이 실제 구글 시트 하단 탭 이름과 정확히 일치해야 합니다.
        df_kpi = conn.read(spreadsheet=SHEET_URL, worksheet="KPI", ttl=0)
        df_region = conn.read(spreadsheet=SHEET_URL, worksheet="지역", ttl=0)
        df_age = conn.read(spreadsheet=SHEET_URL, worksheet="연령", ttl=0)
        return df_kpi, df_region, df_age
    except Exception as e:
        st.error(f"⚠️ 데이터 로드 실패: 시트 이름('KPI', '지역', '연령')이나 권한을 확인하세요.")
        st.stop() # 데이터가 없으면 여기서 실행 중단

# 데이터 불러오기
df_kpi, df_region, df_age = load_data()

# 3. 스트림릿 탭 구성
tab1, tab2, tab3 = st.tabs(["📈 핵심 지표(KPI)", "🗺️ 지역별 성장률", "👥 연령대별 비중"])

# --- TAB 1: KPI 분석 ---
with tab1:
    st.subheader("주요 성과 지표")
    k_cols = st.columns(4)
    
    # 지표 자동 배치 (에러 방지를 위해 데이터가 충분한지 확인)
    for i in range(min(len(df_kpi), 4)):
        with k_cols[i]:
            st.metric(
                label=df_kpi.iloc[i]['label'], 
                value=df_kpi.iloc[i]['value'], 
                delta=df_kpi.iloc[i]['delta']
            )
    
    st.divider()
    st.info("🤖 **AI 마케팅 요약**")
    # A7 셀 부근의 AI 요약 데이터 표시
    if len(df_kpi) >= 6:
        ai_summary = df_kpi.iloc[5, 0]
        st.write(ai_summary)

# --- TAB 2: 지역별 분석 ---
with tab2:
    st.subheader("지역 및 채널별 성장률 분석")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        fig_region = px.bar(df_region, x="지역", y="성장률", 
                            color="지역", text_auto=True,
                            title="지역별 전주 대비 성장 추이(%)")
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col_right:
        st.write("**지역별 인사이트**")
        max_region = df_region.sort_values('성장률', ascending=False).iloc[0]['지역']
        st.markdown(f"- **최대 성장:** {max_region}")

# --- TAB 3: 연령별 분석 ---
with tab3:
    st.subheader("구매 고객 연령대 분포")
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        fig_age = px.pie(df_age, values="비중", names="연령대", 
                         title="연령대별 구매 비중", hole=0.4)
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col_r:
        st.write("**타겟 세부 분석**")
        st.success(f"주력 소비층: **{df_age.iloc[0]['연령대']}**")
