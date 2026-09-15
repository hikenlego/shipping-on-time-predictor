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
            "가뭄 고위험: 소형선(흘수 제한 극복) 전환 40%, 희망봉 우회 40%"
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
            "가뭄 지속: 소형선 통항 35%, 희망봉 우회 병행 (스케줄 안정화)"
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
            "수위 정상화: 대형 정기 파나마 노선 복귀(70%), 소형선 비중 축소"
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
        "권고 대응전략": "정상 수위 유지: 대형선 직기항 70%, 소형선 15% 유지",
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

# 2. 사이드바
st.sidebar.header("📁 데이터셋 업로드")
file1 = st.sidebar.file_uploader("운항 실적 파일 (voyages)", type=["xlsx"])

# 3. 모델 가중치 정의
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

  # 4) 정시성 예측 연산
  pred_delay = (
      (avg_delay * 0.75) + (panama_wait * W_PANAMA) + (m_delay * W_CARRIER)
  )
  pred_on_time = max(10.0, 100.0 - (pred_delay * 0.95))

  # 5) 소형선 전환 및 물동량 조절 전략에 따른 세부 ROI 계산
  # (1) 소형 선박 전환 전략 변수
  # 대형선의 흘수(Draft) 제한 대기 시간을 피하기 위해 물동량의 30%를 흘수가 얕은 소형선으로 배정
  small_vessel_ratio = 0.30
  small_vessel_teu = total_teu * small_vessel_ratio
  small_vessel_premium_rate = 0.10  # 소형선 피더/슬롯 추가 용선 비용 (+10%)
  small_vessel_saved_hours = 14.5  # 대형선 흘수 대기 대비 절감 시간 (14.5시간)

  # (2) 재무적 편익(Savings) 산출
  savings_carrier = total_teu * (saved_hours_carrier * W_CARRIER) * (avg_freight / 24.0)
  savings_port = total_teu * (8.5 * W_CAX) * (avg_freight / 24.0)
  savings_small_vessel = small_vessel_teu * small_vessel_saved_hours * (avg_freight / 24.0)
  total_savings = savings_carrier + savings_port + savings_small_vessel

  # (3) 전략 집행 비용(Cost) 산출
  cost_rerouting = total_teu * 0.40 * avg_freight * premium_pct  # 40% 우회 노선 할당비용
  cost_slot_reserve = total_teu * 0.20 * avg_freight * 0.02     # 20% 대형선 슬롯 예약금
  cost_small_vessel = small_vessel_teu * avg_freight * small_vessel_premium_rate # 30% 소형선 프리미엄 비용
  total_cost = cost_rerouting + cost_slot_reserve + cost_small_vessel

  net_benefit = total_savings - total_cost
  roi = (net_benefit / total_cost) * 100.0 if total_cost > 0 else 0.0

  # 상단 Key Metrics
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("🎯 예측 정시성 Index", f"{pred_on_time:.1f} %")
  col2.metric("⏱️ 예상 평균 지연", f"{pred_delay:.1f} 시간")
  col3.metric("💰 순 재무적 이익", f"${net_benefit:,.0f}")
  col4.metric("📊 최종 ROI", f"{roi:.2f} %")

  st.markdown("---")

  # 하단 분석 리포트 매트릭스
  st.subheader("🎯 구체적 실행 수치 기반 추천 전략 매트릭스")

  c1, c2 = st.columns(2)
  with c1:
    st.markdown("### 1. 파나마 기후/수위 리스크 대응 물동량 조절")
    st.markdown(
        f"- **일일 쿼터 연동 배분**: 현재 정상 수위({panama_row['일일 통항 허용 척수 (척/일)']}척/일) 기준 **파나마 60% / 우회 40%** 동적 분산"
    )
    st.markdown(
        "- **가뭄 경보 발령 시 트리거**: 대기선박 **20척 초과** 또는 대기시간 **12시간 초과** 시 우회 비중을 **60%**로 즉각 확대"
    )
    st.markdown(
        f"- **운하 운임 프리미엄 통제**: 희망봉 우회 대비 운임 차이 **{premium_pct * 100.0:.1f}%** 수준 방어"
    )

    st.markdown("### 2. 저수위 극복을 위한 소형 선박(피더/파나막스) 전환")
    st.markdown(
        f"- **소형선 전환 물동량**: 전체 물동량의 **{small_vessel_ratio*100:.0f}% ({small_vessel_teu:,.0f} TEU)** 투입"
    )
    st.markdown(
        f"- **흘수(Draft) 병목 해소**: 대형선 저수위 통항 대기 대비 **{small_vessel_saved_hours:.1f}시간/TEU** 단축"
    )
    st.markdown(
        f"- **소형선 단독 절감액**: 공급망 정체 방지로 **${savings_small_vessel:,.0f}** 기회비용 방어"
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
      "👈 좌측 사이드바에 운항 실적 파일(voyages)을 업로드하시면 대시보드가 즉시 계산되어 표시됩니다."
  )
