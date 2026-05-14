import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(page_title="KGC 실시간 마케팅 대시보드", layout="wide")

st.title("🚀 정관장 에브리타임 밸런스 성과 대시보드")
st.markdown("### 구글 스프레드시트 데이터 실시간 연동 중")
st.divider()

# 2. 구글 스프레드시트 연결 및 데이터 로드
# Secrets에 설정된 정보를 바탕으로 연결합니다.
conn = st.connection("gsheets", type=GSheetsConnection)

# 여기에 사용 중인 구글 스프레드시트의 전체 URL을 입력하세요.
SHEET_URL = "https://docs.google.com/spreadsheets/d/12G7u0kwszplju89"

try:
    # 데이터 읽어오기 (image_bcd6e1.png의 구조를 반영)
    # ttl=0은 테스트를 위해 캐시를 사용하지 않고 즉시 새로고침한다는 의미입니다.
    df = conn.read(spreadsheet=SHEET_URL, ttl=0)

    # 3. 핵심 지표 (KPI Metrics) - 시트의 데이터를 순서대로 매핑
    col1, col2, col3, col4 = st.columns(4)
    
    # 각 컬럼에 시트의 0~3행 데이터를 배치합니다.
    with col1:
        st.metric(label=df.iloc[0]['label'], value=df.iloc[0]['value'], delta=df.iloc[0]['delta'])
    with col2:
        # 퍼센트 형식(30.00%)이 문자열로 들어올 경우를 대비해 그대로 표시합니다.
        st.metric(label=df.iloc[1]['label'], value=df.iloc[1]['value'], delta=df.iloc[1]['delta'])
    with col3:
        st.metric(label=df.iloc[2]['label'], value=df.iloc[2]['value'], delta=df.iloc[2]['delta'])
    with col4:
        st.metric(label=df.iloc[3]['label'], value=df.iloc[3]['value'], delta=df.iloc[3]['delta'])

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("구글 시트의 공유 설정과 서비스 계정 권한을 다시 확인해주세요.")

st.divider()

# 4. 분석 가설 및 차트 (기존 로직 유지 또는 데이터 기반 확장)
st.subheader("💡 데이터 기반 마케팅 인사이트")
c1, c2 = st.columns(2)

with c1:
    st.info("**지역별 성과 분석 가설**")
    st.write("- 수도권 판매량 지표가 **" + str(df.iloc[0]['value']) + "**로 나타남에 따라 편의점 채널의 지배력 확인.")
    st.write("- 지방 대형마트의 정체 원인을 규명하기 위한 추가 샘플링 조사 필요.")

with c2:
    st.success("**아웃도어 트렌드 결합**")
    st.write(f"- {df.iloc[2]['label']} 지표가 {df.iloc[2]['value']} 수준으로 상승.")
    st.write("- 등산 및 테니스 동호회를 타겟으로 한 앰배서더 마케팅 강화 제언.")

# 5. 하단 액션 플랜 체크리스트
st.divider()
st.subheader("🎯 향후 추진 과제")
st.checkbox("가격 저항선 완화를 위한 2030 전용 구독 서비스 검토", value=True)
st.checkbox("패키지 개봉 편의성 개선을 위한 샘플 테스트 진행")
