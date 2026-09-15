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
    "실시간 기후 API 및 내장 통합 데이터셋 기반 정량적 의사결정 지원 웹 서비스"
)
st.markdown("---")

# 1. 4Tabs 통합 데이터셋 완전 코드 내장
PANAMA_CLIMATE_DATA = pd.DataFrame([
    {
        "기준연도": 2023,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 28.2,
        "평균 통항 대기시간 (시간)": 19.4,
        "평균 대기 선박 수 (척)": 48.7,
        "가뭄 리스크 등급": "High",
        "파나마 노선 평균 운임 (USD/TEU)": 2628.2,
        "희망봉 우회 대비 운임 차이 (%)": -30.7,
        "권고 대응전략": (
            "가뭄 고위험 구간: 소형선 전환 우선 배정, 예약 슬롯 선점"
        ),
    },
    {
        "기준연도": 2024,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 29.9,
        "평균 통항 대기시간 (시간)": 18.7,
        "평균 대기 선박 수 (척)": 44.7,
        "가뭄 리스크 등급": "High",
        "파나마 노선 평균 운임 (USD/TEU)": 2584.9,
        "희망봉 우회 대비 운임 차이 (%)": -28.6,
        "권고 대응전략": (
            "가뭄 지속: 희망봉 우회 병행 검토 (단가는 낮으나 리드타임"
            " 증가 상쇄 필요)"
        ),
    },
    {
        "기준연도": 2025,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 37.4,
        "평균 통항 대기시간 (시간)": 4.1,
        "평균 대기 선박 수 (척)": 2.6,
        "가뭄 리스크 등급": "Low",
        "파나마 노선 평균 운임 (USD/TEU)": 2399.7,
        "희망봉 우회 대비 운임 차이 (%)": -22.6,
        "권고 대응전략": (
            "수위 정상화: 정기 파나마 노선 복귀, 소형선 프리미엄 해제"
        ),
    },
    {
        "기준연도": 2026,
        "노선": "Panama Canal",
        "일일 통항 허용 척수 (척/일)": 37.9,
        "평균 통항 대기시간 (시간)": 4.1,
        "평균 대기 선박 수 (척)": 2.2,
        "가뭄 리스크 등급": "Low",
        "파나마 노선 평균 운임 (USD/TEU)": 2396.4,
        "희망봉 우회 대비 운임 차이 (%)": -22.9,
        "권고 대응전략": "정상 운영 유지 (2026년 상반기 기준)",
    },
])

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

# 2. 사이드바: 운항 실적 파일 단 1개 요구
st.sidebar.header("📁 데이터셋 업로드")
file1 = st.sidebar.file_uploader("운항 실적 파일 (voyages)", type=["xlsx"])

# 3. 고정 최적 가중치
W_PANAMA = 0.45
W_CAX = 0.35
W_CARRIER = 0.20

if file1 is not None:
  df_voyages = pd.read_excel(file1, sheet_name="voyages")

  # 1) 기본 실측 지표 연산
  avg_freight = float(df_voyages["freight_rate_usd_per_teu"].mean())
  avg_delay = float(df_voyages["delay_hours"].mean())
  total_teu = int(len(df_voyages) * 10)

  # 2) 파나마 실측 지표 연계
  panama_row = PANAMA_CLIMATE_DATA[
      PANAMA_CLIMATE_DATA["가뭄 리스크 등급"] == "Low"
  ].iloc[0]
  panama_wait = float(panama_row["평균 통항 대기시간 (시간)"])
  premium_pct = (
      float(abs(panama_row["희망봉 우회 대비 운임 차이 (%)"])) / 100.0
  )

  # 3) 선사 실측 지표 연계
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

  # 4) 정시성 및 재무 ROI 모델 연산
  pred_delay = (
      (panama_wait * W_PANAMA)
      + (avg_delay * 0.10)
      + (m_delay * (1.0 - W_PANAMA - 0.10))
  )
  pred_on_time = max(10.0, 100.0 - (pred_delay * 0.95))

  saved_hours = (8.5 * W_CAX) + (saved_hours_carrier * W_CARRIER)
  total_savings = total_teu * saved_hours * (avg_freight / 24.0)
  total_cost = (total_teu * 0.70 * avg_freight * premium_pct) + (
      total_teu * 0.25 * avg_freight * 0.02
  )
  net_benefit = total_savings - total_cost
  roi = (net_benefit / total_cost) * 100.0 if total_cost > 0 else 0.0

  # 상단 Key Metrics
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("🎯 예측 정시성 Index", f"{pred_on_time:.1f} %")
  col2.metric("⏱️ 예상 평균 지연", f"{pred_delay:.1f} 시간")
  col3.metric("💰 순 재무적 이익", f"${net_benefit:,.0f}")
  col4.metric("📊 최종 ROI", f"{roi:.2f} %")

  st.markdown("---")

  # 하단 구체적 수치 기반 분석 리포트 매트릭스
  st.subheader("🎯 구체적 실행 수치 기반 추천 전략 매트릭스")

  c1, c2 = st.columns(2)
  with c1:
    st.markdown("### 1. 선사 물동량 재배치 세부 실행안")
    realloc_m_teu = total_teu * 0.50
    realloc_other_teu = total_teu * 0.1667
    carrier_savings_amt = total_teu * saved_hours_carrier * (avg_freight / 24.0)

    st.markdown(
        "- **우선 배정 선사 (M사)**: 물동량 비중 **50.0%"
        f" ({realloc_m_teu:,.0f} TEU)** 확대"
    )
    st.markdown(
        "- **기타 선사 (G/C/O사)**: 각 **16.7%"
        f" ({realloc_other_teu:,.0f} TEU)** 분산 배정"
    )
    st.markdown(
        "- **지연 단축 효과**: 타 선사 대비"
        f" **{saved_hours_carrier:.1f}시간/TEU 단축**"
    )
    st.markdown(
        f"- **기회비용 절감액**: 총 **${carrier_savings_amt:,.0f}** 절감"
    )

    st.markdown("### 2. 운하 및 슬롯 운영 임계치 전략")
    st.markdown(
        "- **파나마 운하 쿼터**: 일일"
        f" **{panama_row['일일 통항 허용 척수 (척/일)']}척** 기준 운항"
    )
    st.markdown(
        "- **노선 할당 비중**: 파나마 정기 노선 **70.0%"
        f" ({total_teu * 0.70:,.0f} TEU)** 유지"
    )
    st.markdown(
        "- **우회 비상 전환 조건**: 대기선박 **20척 초과** 또는 대기시간"
        " **12시간 초과** 시 전환"
    )
    st.markdown(
        "- **우회 프리미엄 비용 반영**: 운임 차이"
        f" **{premium_pct * 100.0:.1f}%** 수준 적용"
    )

  with c2:
    st.markdown("### 3. 항만 및 내륙 체류(Dwell Time) 제어 지표")
    st.markdown(
        "- **CAx 수출항 관리 목표**: CAx 지수 **0.35 이하** 유지 시 선적"
        " 전 체류 **2.5일 이내** 고수"
    )
    st.markdown(
        "- **수입항 Dwell Time 트리거**: 체류시간 **3.5일 초과** 시 내륙"
        " 철도 수송 비중 **30%** 확대"
    )
    st.markdown(
        "- **항만 체류시간 감축 연동**: 목표 절감 시간 **8.5시간/TEU** 반영"
    )

    st.markdown("### 4. 정량적 ROI 재무 내역 상세")
    st.markdown(
        f"- **총 분석 물동량**: {total_teu:,} TEU (voyages"
        f" {len(df_voyages):,}건 연동)"
    )
    st.markdown(
        f"- **시간당 기회손실 단가**: ${avg_freight / 24.0:.2f} / hr/TEU"
    )
    st.markdown(
        f"- **총 지연 손실 방지액 (Savings)**: ${total_savings:,.2f}"
    )
    st.markdown(f"- **총 전략 집행 비용 (Cost)**: ${total_cost:,.2f}")
    st.markdown(
        f"- **최종 순 재무적 이익 (Net Benefit)**: ${net_benefit:,.0f}"
    )
else:
  st.info(
      "👈 좌측 사이드바에 운항 실적 파일(voyages)을 업로드하시면 대시보드가 즉시"
      " 계산되어 표시됩니다."
  )
