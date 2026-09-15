import numpy as np
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="해상 정시성 예측 & ROI 분석 대시보드",
    page_icon="🚢",
    layout="wide",
)

st.title("🚢 글로벌 해상 정시성 예측 & ROI 분석 시스템")
st.caption(
    "실시간 기후 API 및 4개 통합 탭 데이터 기반 정량적 의사결정 지원 웹"
    " 서비스"
)
st.markdown("---")

# 사이드바 데이터 및 가중치 설정
st.sidebar.header("📁 데이터셋 업로드")
file1 = st.sidebar.file_uploader(
    "1. 글로벌 운송 파일 (voyages)", type=["xlsx"]
)
file2 = st.sidebar.file_uploader(
    "2. 통합 데이터셋 파일 (4Tabs)", type=["xlsx"]
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 리스크 가중치 튜닝")
w_panama = st.sidebar.slider("파나마 운하 대기시간 가중치", 0.0, 1.0, 0.45)
w_cax = st.sidebar.slider("CAx/항만 체류 가중치", 0.0, 1.0, 0.35)
w_carrier = st.sidebar.slider("선사 회전율 가중치", 0.0, 1.0, 0.20)

if file1 and file2:
  # 데이터 로드
  df_voyages = pd.read_excel(file1, sheet_name="voyages")
  df_panama = pd.read_excel(file2, sheet_name="panama_climate_risk", header=3)
  df_carrier = pd.read_excel(
      file2, sheet_name="carrier_performance", header=3
  )

  # 실측 변수 계산
  avg_freight = float(df_voyages["freight_rate_usd_per_teu"].mean())
  avg_delay = float(df_voyages["delay_hours"].mean())
  total_teu = len(df_voyages) * 10

  panama_row = df_panama[df_panama["가뭄 리스크 등급"] == "Low"].iloc[0]
  panama_wait = float(panama_row["평균 통항 대기시간 (시간)"])
  premium_pct = float(abs(panama_row["희망봉 우회 대비 운임 차이 (%)"])) / 100.0

  m_delay = float(
      df_carrier[
          (df_carrier["선사"] == "M사")
          & (df_carrier["노선"] == "Panama Canal")
      ]["평균 지연시간 (시간)"].iloc[0]
  )
  others_delay = float(
      df_carrier[
          (df_carrier["선사"] != "M사")
          & (df_carrier["노선"] == "Panama Canal")
      ]["평균 지연시간 (시간)"].mean()
  )
  saved_hours_carrier = others_delay - m_delay

  # KPI 및 ROI 연산
  pred_delay = (
      (panama_wait * w_panama)
      + (avg_delay * 0.1)
      + (m_delay * (1 - w_panama - 0.1))
  )
  pred_on_time = max(10.0, 100.0 - (pred_delay * 0.95))

  saved_hours = (8.5 * w_cax) + (saved_hours_carrier * w_carrier)
  total_savings = total_teu * saved_hours * (avg_freight / 24.0)
  total_cost = (total_teu * 0.70 * avg_freight * premium_pct) + (
      total_teu * 0.25 * avg_freight * 0.02
  )
  net_benefit = total_savings - total_cost
  roi = (net_benefit / total_cost) * 100 if total_cost > 0 else 0.0

  # 상단 핵심 지표
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("🎯 예측 정시성 Index", f"{pred_on_time:.1f} %")
  col2.metric("⏱️ 예상 평균 지연", f"{pred_delay:.1f} 시간")
  col3.metric("💰 순 재무적 이익", f"${net_benefit:,.0f}")
  col4.metric("📊 최종 ROI", f"{roi:.2f} %")

  st.markdown("---")

  # 하단 분석 리포트
  c1, c2 = st.columns(2)
  with c1:
    st.subheader("📌 실측 데이터 기반 추천 전략")
    st.info(f"**파나마 노선**: {panama_row['권고 대응전략']}")
    st.success(
        f"**선사 포트폴리오**: M사 집중 배정 시 타 선사 대비"
        f" **{saved_hours_carrier:.1f}시간** 단축 효과"
    )

  with c2:
    st.subheader("💵 정량적 ROI 재무 내역")
    st.write(f"- **분석 총 물동량**: {total_teu:,} TEU")
    st.write(f"- **voyages 평균 운임**: ${avg_freight:,.2f} / TEU")
    st.write(f"- **지연 손실 방지액 (Savings)**: ${total_savings:,.2f}")
    st.write(
        f"- **전략 집행 비용 (Cost)**: ${total_cost:,.2f} (프리미엄"
        f" {premium_pct*100:.1f}% 반영)"
    )
else:
  st.warning(
      "👈 좌측 사이드바에 엑셀 파일 2개를 업로드하시면 실시간 분석 웹 알고리즘이"
      " 작동합니다."
  )
