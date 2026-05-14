import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(page_title="KGC 통합 마케팅 분석", layout="wide")
st.title("📊 정관장 에브리타임 밸런스 실시간 리포트")

# 2. 구글 스프레드시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)
SHEET_URL = "https://docs.google.com/spreadsheets/d/12G7u0kwszplju89Qkj4MI_0O9X7H2F8u-Tb9DEB6-yY/edit?gid=0#gid=0"

# 각 시트(Worksheet)별 데이터 로드
try:
    df_kpi = conn.read(spreadsheet=SHEET_URL, worksheet="KPI", ttl=0)
    df_region = conn.read(spreadsheet=SHEET_URL, worksheet="지역", ttl=0)
    df_age = conn.read(spreadsheet=SHEET_URL, worksheet="연령", ttl=0)
except Exception as e:
    st.error(f"데이터 로드 실패: 시트 이름('KPI', '지역', '연령')이 정확한지 확인해 주세요.")

# 3. 스트림릿 탭 구성 (시트 구조와 동일하게)
tab1, tab2, tab3 = st.tabs(["📈 핵심 지표(KPI)", "🗺️ 지역별 성장률", "👥 연령대별 비중"])

# --- TAB 1: KPI 분석 ---
with tab1:
    st.subheader("주요 성과 지표")
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)
    
    # 지표 자동 배치
    cols = [k_col1, k_col2, k_col3, k_col4]
    for i in range(4):
        with cols[i]:
            st.metric(label=df_kpi.iloc[i]['label'], 
                      value=df_kpi.iloc[i]['value'], 
                      delta=df_kpi.iloc[i]['delta'])
    
    st.divider()
    # 시트 A7 셀의 AI 요약 내용 표시 (에러 메시지 대신 요약 결과가 나오도록 구성)
    st.info("🤖 **AI 마케팅 요약**")
    ai_summary = df_kpi.iloc[5, 0] # 시트의 7번째 행(A7) 데이터
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
        st.markdown(f"""
        - **최대 성장:** {df_region.sort_values('성장률', ascending=False).iloc[0]['지역']}
        - **현황:** 편의점 채널의 압도적 강세가 수도권 성장을 견인 중입니다.
        """)

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
        target_age = df_age.iloc[0]['연령대']
        target_ratio = df_age.iloc[0]['비중']
        st.success(f"현재 주력 소비층은 **{target_age}** ({target_ratio})입니다.")
        st.write("2030 사회초년생의 '갓생' 트렌드에 맞춘 마케팅 메시지 유효성 입증.")
