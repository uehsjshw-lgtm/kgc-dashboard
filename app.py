import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="마케팅 전략 대시보드", layout="wide")

st.title("🚀 정관장 에브리타임 밸런스 리뉴얼 성과 분석")
st.markdown("### 2026년 3월 4주차 | 마케팅 가설 및 데이터 인사이트")
st.divider()

# 2. 핵심 지표 (KPI Metrics)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="전체 판매량 추이", value="+13%", delta="수도권 강세")
with col2:
    st.metric(label="2030 구매 비중", value="45%", delta="주력 타겟층")
with col3:
    st.metric(label="아웃도어 키워드 언급", value="+30%", delta="등산/테니스")
with col4:
    st.metric(label="리뷰 긍정률", value="78%", delta="맛/디자인 만족")

st.divider()

# 3. 판매 실적 분석 (Chart & Hypotheses)
st.subheader("📍 지역별/채널별 판매 실적 비교")
col_left, col_right = st.columns([2, 1])

with col_left:
    # 데이터 생성
    sales_data = pd.DataFrame({
        "지역": ["수도권(편의점)", "지방(대형마트)"],
        "증감률(%)": [15, -2]
    })
    fig = px.bar(sales_data, x="지역", y="증감률(%)", color="지역", 
                 text_auto=True, title="전주 대비 판매 증감률",
                 color_discrete_map={"수도권(편의점)": "#EF553B", "지방(대형마트)": "#636EFA"})
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.info("💡 **실적 격차 가설 (추정 원인)**")
    with st.expander("수도권 편의점 강세 이유"):
        st.write("""
        - **라이프스타일 점유:** 2030 사회초년생의 '갓생' 트렌드와 편의점 접근성 결합.
        - **디자인 효과:** 리뉴얼 패키지가 젊은 층의 즉흥적 구매 유도.
        """)
    with st.expander("지방 대형마트 정체 이유"):
        st.write("""
        - **타겟 불일치:** 마트 주 고객(4050)은 '부드러운 맛'보다 '고함량' 선호 가능성.
        - **인지도 전이 지연:** 신규 리뉴얼 메시지의 지방 확산 속도 차이.
        """)

st.divider()

# 4. 고객 리뷰 및 키워드 분석
st.subheader("💬 고객 보이스 및 키워드 트렌드")
col_rev1, col_rev2 = st.columns(2)

with col_rev1:
    # 감성 분석 차트
    sentiment_data = pd.DataFrame({
        "구분": ["긍정(맛/디자인)", "부정(가격/개봉)", "중립"],
        "비중": [70, 20, 10]
    })
    fig_pie = px.pie(sentiment_data, values="비중", names="구분", title="고객 리뷰 감성 분포",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_rev2:
    st.warning("⚠️ **주요 리스크 가설 (추정 원인)**")
    st.markdown("""
    *   **가격 체감도:** 리뉴얼 후 할인 프로모션 축소로 인한 민감도 상승 추정.
    *   **패키지 이슈:** 신규 지질 또는 코팅 방식이 개봉 시 마찰력을 높였을 가능성.
    """)
    st.success("🎾 **기회 요인: 아웃도어 트렌드**")
    st.write("등산/테니스 키워드 30% 증가 → '운동 전 에너지 부스팅' 아이템으로 인식 확산 중.")

# 5. 전략 제언 액션 플랜
st.divider()
st.subheader("🎯 베테랑 마케터의 전략 제언")
st.checkbox("수도권: 테니스장/등산로 인근 편의점 '오운완' 팝업 매대 설치")
st.checkbox("지방: 대형마트 내 '쓴맛 완화' 강조 시음 행사 및 가족 패키지 강화")
st.checkbox("QC: 패키지 개봉선(Perforation) 기술 보완 검토 요청")

st.sidebar.title("설정")
st.sidebar.info("본 대시보드는 가설 중심의 초안입니다. 실제 원인 파악 후 데이터를 업데이트하세요.")
