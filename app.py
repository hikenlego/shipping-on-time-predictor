import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="해상 정시성 예측 & ROI 분석 대시보드",
    page_icon="🚢",
    layout="wide",
)

st.title("🚢 글로벌 해상 정시성 예측 & ROI 분석 시스템")
st.caption(
    "실시간 기후 API 및 4개 통합 탭 데이터셋 기반 정량적 의사결정 지원 웹 서비스"
)
st.markdown("---")

# ==============================================================================
# 1. 4Tabs 통합 데이터셋 완전 코드 내장
# ==============================================================================

# Tab 1: 파나마 기후 및 운하 수위 리스크
PANAMA_CLIMATE_DATA = pd.DataFrame([
    {
        "기준연도": 2023,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 24.0,
        "평균 통항 대기시간 (시간)": 20.5,
        "평균 대기 선박 수 (척)": 52.0,
        "가뭄 리스크 등급": "High",
        "파나마 노선 평균 운임 (USD/TEU)": 2680.5,
        "희망봉 우회 대비 운임 차이 (%)": -32.5,
        "권고 대응전략": "가뭄 극심기: 소형선(흘수 극복) 40% 전환 및 희망봉 우회 40% 배정",
    },
    {
        "기준연도": 2024,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 28.5,
        "평균 통항 대기시간 (시간)": 15.2,
        "평균 대기 선박 수 (척)": 38.0,
        "가뭄 리스크 등급": "High",
        "파나마 노선 평균 운임 (USD/TEU)": 2550.0,
        "희망봉 우회 대비 운임 차이 (%)": -27.0,
        "권고 대응전략": "가뭄 지속기: 소형선 35% 투입 및 예약 슬롯 경매 선점",
    },
    {
        "기준연도": 2025,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 34.0,
        "평균 통항 대기시간 (시간)": 4.5,
        "평균 대기 선박 수 (척)": 4.2,
        "가뭄 리스크 등급": "Low",
        "파나마 노선 평균 운임 (USD/TEU)": 2400.0,
        "희망봉 우회 대비 운임 차이 (%)": -22.0,
        "권고 대응전략": "수위 회복기: 정기 파나마 노선 복귀(대형선 70%), 소형선 비중 축소",
    },
    {
        "기준연도": 2026,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 36.0,
        "평균 통항 대기시간 (시간)": 3.8,
        "평균 대기 선박 수 (척)": 2.5,
        "가뭄 리스크 등급": "Low",
        "파나마 노선 평균 운임 (USD/TEU)": 2380.0,
        "희망봉 우회 대비 운임 차이 (%)": -21.5,
        "권고 대응전략": "정상 운영기: 표준 스케줄 유지 및 대형선 직기항 70% 운영",
    },
])

# Tab 2: 항만 혼잡도 및 CAx 컨테이너 체류 데이터
CAX_DWELL_DATA = pd.DataFrame([
    {
        "항만": "Busan",
        "권역": "Asia Origin",
        "평균 CAx 지수": 0.32,
        "수출 컨테이너 체류일수 (일)": 2.4,
        "수입 컨테이너 체류일수 (일)": 2.8,
        "선석 대기시간 (시간)": 6.5,
        "혼잡도 등급": "Low",
        "권고 전략": "수출 컨테이너 선적 전 체류 2.5일 이내 엄수",
    },
    {
        "항만": "Shanghai",
        "권역": "Asia Origin",
        "평균 CAx 지수": 0.45,
        "수출 컨테이너 체류일수 (일)": 3.2,
        "수입 컨테이너 체류일수 (일)": 3.5,
        "선석 대기시간 (시간)": 12.0,
        "혼잡도 등급": "Moderate",
        "권고 전략": "환적 피더선 배정 및 얼라이언스 선복 공유",
    },
    {
        "항만": "Rotterdam",
        "권역": "EU Destination",
        "평균 CAx 지수": 0.58,
        "수출 컨테이너 체류일수 (일)": 3.8,
        "수입 컨테이너 체류일수 (일)": 4.5,
        "선석 대기시간 (시간)": 18.5,
        "혼잡도 등급": "High",
        "권고 전략": "Dwell Time 3.5일 초과 시 내륙 바지선/철도 복합운송 30% 전환",
    },
    {
        "항만": "New York",
        "권역": "USEC Destination",
        "평균 CAx 지수": 0.62,
        "수출 컨테이너 체류일수 (일)": 4.1,
        "수입 컨테이너 체류일수 (일)": 4.8,
        "선석 대기시간 (시간)": 22.0,
        "혼잡도 등급": "High",
        "권고 전략": "야간 게이트 반입 및 내륙 철도 인터모달 운송 직결",
    },
])

# Tab 3: 선사별 노선 운항 실적 및 지연 편차 데이터
CARRIER_PERFORMANCE_DATA = pd.DataFrame([
    {
        "선사": "M사",
        "노선": "Suez Canal",
        "표본 항해 수 (건)": 145,
        "평균 회전율 (일)": 37.8,
        "평균 지연시간 (시간)": 44.2,
        "24시간 초과 지연 비율 (%)": 78.6,
        "평균 운임 (USD/TEU)": 2536.5,
    },
    {
        "선사": "M사",
        "노선": "Panama Canal",
        "표본 항해 수 (건)": 922,
        "평균 회전율 (일)": 28.0,
        "평균 지연시간 (시간)": 48.7,
        "24시간 초과 지연 비율 (%)": 73.0,
        "평균 운임 (USD/TEU)": 2502.1,
    },
    {
        "선사": "M사",
        "노선": "Cape of Good Hope",
        "표본 항해 수 (건)": 774,
        "평균 회전율 (일)": 49.5,
        "평균 지연시간 (시간)": 37.1,
        "24시간 초과 지연 비율 (%)": 55.7,
        "평균 운임 (USD/TEU)": 1849.6,
    },
    {
        "선사": "G사",
        "노선": "Suez Canal",
        "표본 항해 수 (건)": 387,
        "평균 회전율 (일)": 37.5,
        "평균 지연시간 (시간)": 60.8,
        "24시간 초과 지연 비율 (%)": 99.5,
        "평균 운임 (USD/TEU)": 2671.9,
    },
    {
        "선사": "G사",
        "노선": "Panama Canal",
        "표본 항해 수 (건)": 922,
        "평균 회전율 (일)": 27.7,
        "평균 지연시간 (시간)": 64.4,
        "24시간 초과 지연 비율 (%)": 98.8,
        "평균 운임 (USD/TEU)": 2484.3,
    },
    {
        "선사": "G사",
        "노선": "Cape of Good Hope",
        "표본 항해 수 (건)": 531,
        "평균 회전율 (일)": 49.6,
        "평균 지연시간 (시간)": 62.9,
        "24시간 초과 지연 비율 (%)": 99.1,
        "평균 운임 (USD/TEU)": 1849.7,
    },
    {
        "선사": "C사",
        "노선": "Panama Canal",
        "표본 항해 수 (건)": 922,
        "평균 회전율 (일)": 27.7,
        "평균 지연시간 (시간)": 67.2,
        "24시간 초과 지연 비율 (%)": 99.8,
        "평균 운임 (USD/TEU)": 2484.3,
    },
    {
        "선사": "O사",
        "노선": "Panama Canal",
        "표본 항해 수 (건)": 922,
        "평균 회전율 (일)": 27.8,
        "평균 지연시간 (시간)": 67.0,
        "24시간 초과 지연 비율 (%)": 99.7,
        "평균 운임 (USD/TEU)": 2484.3,
    },
])

# Tab 4: 수에즈 vs 희망봉 우회 노선 분석 데이터
SUEZ_CAPE_DATA = pd.DataFrame([
    {
        "구분": "정상 항로 (Suez Canal)",
        "표준 항해일수 (일)": 30.0,
        "추가 항해거리 (nm)": 0,
        "유류비 및 운임 지수": 100.0,
        "지연 위험 요인": "홍해 안보 분쟁 및 전쟁위험보험료 가산",
    },
    {
        "구분": "우회 항로 (Cape of Good Hope)",
        "표준 항해일수 (일)": 42.0,
        "추가 항해거리 (nm)": 3500,
        "유류비 및 운임 지수": 128.5,
        "지연 위험 요인": "항해거리 증가에 따른 리드타임 버퍼 확보 필요",
    },
])

# ==============================================================================
# 2. 사이드바 설정
# ==============================================================================
st.sidebar.header("📁 데이터셋 업로드")
file1 = st.sidebar.file_uploader("운항 실적 파일 (voyages)", type=["xlsx"])

# 연도별 수위/가뭄 리스크 시나리오 선택
selected_year = st.sidebar.selectbox(
    "분석 기준 연도 (수위/기후 시나리오)", [2023, 2024, 2025, 2026], index=3
)

# 모델 핵심 가중치 정의
W_PANAMA = 0.45
W_CAX = 0.35
W_CARRIER = 0.20

# ==============================================================================
# 3. 알고리즘 연산 및 대시보드 렌더링
# ==============================================================================
if file1 is not None:
    df_voyages = pd.read_excel(file1, sheet_name="voyages")

    # 1) 기본 실측 변수 집계
    avg_freight = float(df_voyages["freight_rate_usd_per_teu"].mean())
    avg_delay = float(df_voyages["delay_hours"].mean())
    total_teu = int(len(df_voyages) * 10)

    # 2) 선택된 연도의 파나마 실측 기후/운하 지표 연계
    panama_row = PANAMA_CLIMATE_DATA[
        PANAMA_CLIMATE_DATA["기준연도"] == selected_year
    ].iloc[0]
    panama_wait = float(panama_row["평균 통항 대기시간 (시간)"])
    premium_pct = float(abs(panama_row["희망봉 우회 대비 운임 차이 (%)"])) / 100.0

    # 3) 선사별 운항 실측 지표 연계
    m_delay = float(
        CARRIER_PERFORMANCE_DATA[
            (CARRIER_PERFORMANCE_DATA["선사"] == "M사")
            & (CARRIER_PERFORMANCE_DATA["노선"] == "Panama Canal")
        ]["평균 지연시간 (시간)"].iloc[0]
    )
    others_delay = float(
        CARRIER_PERFORMANCE_DATA[
            (CARRIER_PERFORMANCE_DATA["선사"] != "M사")
            & (CARRIER_PERFORMANCE_DATA["노선"] == "Panama Canal")
        ]["평균 지연시간 (시간)"].mean()
    )
    saved_hours_carrier = others_delay - m_delay

    # 4) 동적 가중치 기반 정시성 Index 예측 모델
    pred_delay = (
        (avg_delay * 0.75) + (panama_wait * W_PANAMA) + (m_delay * W_CARRIER)
    )
    pred_on_time = max(10.0, 100.0 - (pred_delay * 0.95))

    # 5) 소형선 전환 및 물동량 조절 전략에 따른 세부 ROI 계산
    is_drought = panama_row["가뭄 리스크 등급"] == "High"
    small_vessel_ratio = 0.40 if is_drought else 0.20
    small_vessel_teu = total_teu * small_vessel_ratio
    small_vessel_premium_rate = 0.10
    small_vessel_saved_hours = 14.5

    # 재무적 편익 (Savings)
    savings_carrier = total_teu * (saved_hours_carrier * W_CARRIER) * (avg_freight / 24.0)
    savings_port = total_teu * (8.5 * W_CAX) * (avg_freight / 24.0)
    savings_small_vessel = small_vessel_teu * small_vessel_saved_hours * (avg_freight / 24.0)
    total_savings = savings_carrier + savings_port + savings_small_vessel

    # 전략 집행 비용 (Cost)
    reroute_ratio = 0.40 if is_drought else 0.20
    cost_rerouting = total_teu * reroute_ratio * avg_freight * premium_pct
    cost_slot_reserve = total_teu * 0.20 * avg_freight * 0.02
    cost_small_vessel = small_vessel_teu * avg_freight * small_vessel_premium_rate
    total_cost = cost_rerouting + cost_slot_reserve + cost_small_vessel

    # 순이익 및 최종 ROI
    net_benefit = total_savings - total_cost
    roi = (net_benefit / total_cost) * 100.0 if total_cost > 0 else 0.0

    # 상단 Key Metrics 렌더링
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 예측 정시성 Index", f"{pred_on_time:.1f} %")
    col2.metric("⏱️ 예상 평균 지연", f"{pred_delay:.1f} 시간")
    col3.metric("💰 순 재무적 이익", f"${net_benefit:,.0f}")
    col4.metric("📊 최종 ROI", f"{roi:.2f} %")

    st.markdown("---")

    # 하단 구체적 수치 기반 분석 리포트 매트릭스
    st.subheader(f"🎯 [{selected_year}년 기준] 실측 수위 연동 실행 전략 매트릭스")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 1. 파나마 기후/수위 리스크 대응 물동량 조절")
        st.markdown(
            f"- **일일 쿼터 연동 배분**: 기준연도({panama_row['일일 통항 허용 척수 (척/일)']}척/일) 기준 **파나마 {100 - int(reroute_ratio*100)}% / 우회 {int(reroute_ratio*100)}%** 동적 분산"
        )
        st.markdown(
            f"- **가뭄 등급 판정**: **{panama_row['가뭄 리스크 등급']}** (전략: {panama_row['권고 대응전략']})"
        )
        st.markdown(
            f"- **운하 운임 프리미엄 방어**: 희망봉 우회 대비 운임 차이 **{premium_pct * 100.0:.1f}%** 수준 적용"
        )

        st.markdown("### 2. 저수위 극복을 위한 소형 선박(피더/파나막스) 전환")
        st.markdown(
            f"- **소형선 전환 물동량**: 전체 물동량의 **{small_vessel_ratio*100:.0f}% ({small_vessel_teu:,.0f} TEU)** 투입"
        )
        st.markdown(
            f"- **흘수(Draft) 병목 해소**: 대형선 저수위 통항 대기 대비 **{small_vessel_saved_hours:.1f}시간/TEU** 단축"
        )
        st.markdown(
            f"- **소형선 기회비용 방어액**: 공급망 정체 방지로 **${savings_small_vessel:,.0f}** 절감"
        )

    with c2:
        st.markdown("### 3. 선사 포트폴리오 및 항만 Dwell Time 제어")
        realloc_m_teu = total_teu * 0.50
        st.markdown(
            f"- **우선 배정 선사 (M사)**: 회전율 우수 선사에 **50.0% ({realloc_m_teu:,.0f} TEU)** 집중"
        )
        st.markdown(
            f"- **지연 단축 효과**: 타 선사 대비 **{saved_hours_carrier:.1f}시간/TEU** 절감"
        )
        st.markdown(
            "- **항만 Dwell Time 제어**: 체류 3.5일 초과 시 철도 전환(30%)을 통해 **8.5시간/TEU** 감축"
        )

        st.markdown("### 4. 소형선 전환 반영 재무 ROI 상세 명세")
        st.markdown(
            f"- **총 분석 물동량**: {total_teu:,} TEU (voyages {len(df_voyages):,}건)"
        )
        st.markdown(
            f"- **총 지연 손실 방지액 (Savings)**: **${total_savings:,.2f}** (소형선 방어액 포함)"
        )
        st.markdown(
            f"- **소형선 전환 집행 비용**: **${cost_small_vessel:,.2f}** (TEU당 10% 할증 반영)"
        )
        st.markdown(
            f"- **총 전략 집행 비용 (Cost)**: **${total_cost:,.2f}**"
        )
        st.markdown(
            f"- **최종 순 재무적 이익 (Net Benefit)**: **${net_benefit:,.0f}** (ROI: **{roi:.2f}%**)"
        )
else:
    st.info(
        "👈 좌측 사이드바에 운항 실적 파일(voyages)을 업로드하고 분석 연도를 선택해 주세요."
    )
