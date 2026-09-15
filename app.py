import numpy as np
import pandas as pd
import requests
import streamlit as st
import os

st.set_page_config(
    page_title="해상 정시성 예측 & ROI 분석 대시보드",
    page_icon="🚢",
    layout="wide",
)

st.title("🚢 글로벌 해상 정시성 예측 & ROI 분석 시스템")
st.caption(
    "실시간 기후 API 및 통합 데이터셋 기반 구체적 실행 수치 추천 웹 서비스"
)
st.markdown("---")

# 통합 데이터셋 자동 탑재 처리 (파일이 깃허브 루트에 있는 경우 자동 로드)
INTEGRATED_FILE_PATH = "integrated_dataset.xlsx"
ALT_INTEGRATED_FILE_PATH = "Global_Logistics_Integrated_Dataset_4Tabs (1).xlsx"

df_panama = None
df_cax = None
df_carrier = None
df_suez = None

target_file = None
if os.path.exists(INTEGRATED_FILE_PATH):
    target_file = INTEGRATED_FILE_PATH
elif os.path.exists(ALT_INTEGRATED_FILE_PATH):
    target_file = ALT_INTEGRATED_FILE_PATH

# 사이드바 설정
st.sidebar.header("📁 데이터셋 설정")

if target_file is not None:
    st.sidebar.success("✅ 통합 데이터셋(4Tabs)이 시스템 내에 자동 탑재되었습니다.")
    try:
        df_panama = pd.read_excel(target_file, sheet_name="panama_climate_risk", header=3)
        df_cax = pd.read_excel(target_file, sheet_name="cax_dwell_imbalance", header=3)
        df_carrier = pd.read_excel(target_file, sheet_name="carrier_performance", header=3)
        df_suez = pd.read_excel(target_file, sheet_name="suez_cape_rerouting", header=3)
    except Exception as e:
        st.sidebar.error(f"통합 데이터셋 로드 오류: {e}")
else:
    file2 = st.sidebar.file_uploader("2. 통합 데이터셋 파일 (4Tabs)", type=["xlsx"])
    if file2 is not None:
        df_panama = pd.read_excel(file2, sheet_name="panama_climate_risk", header=3)
        df_cax = pd.read_excel(file2, sheet_name="cax_dwell_imbalance", header=3)
        df_carrier = pd.read_excel(file2, sheet_name="carrier_performance", header=3)
        df_suez = pd.read_excel(file2, sheet_name="suez_cape_rerouting", header=3)

# 파일 1(voyages)은 사용자가 업로드
file1 = st.sidebar.file_uploader(
    "1. 글로벌 운송 파일 (voyages)", type=["xlsx"]
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 리스크 가중치 튜닝")
w_panama = st.sidebar.slider("파나마 운하 대기시간 가중치", 0.0, 1.0, 0.45)
w_cax = st.sidebar.slider("CAx/항만 체류 가중치", 0.0, 1.0, 0.35)
w_carrier = st.sidebar.slider("선사 회전율 가중치", 0.0, 1.0, 0.20)

if file1 and df_panama is not None and df_carrier is not None:
  # 데이터 로드
  df_voyages = pd.read_excel(file1, sheet_name="voyages")

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

  # 하단 구체적 수치 기반 분석 리포트 매트릭스
  st.subheader("🎯 구체적 실행 수치 기반 추천 전략 매트릭스")
  
  c1, c2 = st.columns(2)
  with c1:
    st.markdown("<b>1. 선사 물동량 재배치 세부 실행안</b>", unsafe_allow_html=True)
    realloc_m_teu = total_teu * 0.50
    realloc_other_teu = total_teu * 0.1667
    carrier_savings_amt = total_teu * saved_hours_carrier * (avg_freight / 24.0)
    
    st.write(f"- <b>우선 배정 선사 (M사)</b>: 물동량 비중 <b>50.0% ({realloc_m_teu:,.0f} TEU)</b> 확대")
    st.write(f"- <b>기타 선사 (G/C/O사)</b>: 각 <b>16.7% ({realloc_other_teu:,.0f} TEU)</b> 분산 배정")
    st.write(f"- <b>지연 단축 효과</b>: 타 선사 대비 <b>{saved_hours_carrier:.1f}시간/TEU 단축</b>")
    st.write(f"- <b>기회비용 절감액</b>: 총 <b>${carrier_savings_amt:,.0f}</b> 절감")

    st.markdown("<b>2. 운하 및 슬롯 운영 임계치 전략</b>", unsafe_allow_html=True)
    st.write(f"- <b>파나마 운하 쿼터</b>: 일일 <b>{panama_row['일일 통항 허용 척수 (척/일)']}척</b> 기준 운항")
    st.write(f"- <b>노선 할당 비중</b>: 파나마 정기 노선 <b>70.0% ({total_teu * 0.70:,.0f} TEU)</b> 유지")
    st.write(f"- <b>우회 비상 전환 조건</b>: 대기선박 <b>20척 초과</b> 또는 대기시간 <b>12시간 초과</b> 시 전환")
    st.write(f"- <b>우회 프리미엄 비용 반영</b>: 운임 차이 <b>{premium_pct * 100.0:.1f}%</b> 수준 적용")

  with c2:
    st.markdown("<b>3. 항만 및 내륙 체류(Dwell Time) 제어 지표</b>", unsafe_allow_html=True)
    st.write(f"- <b>CAx 수출항 관리 목표</b>: CAx 지수 <b>0.35 이하</b> 유지 시 선적 전 체류 <b>2.5일 이내</b> 고수")
    st.write(f"- <b>수입항 Dwell Time 트리거</b>: 체류시간 <b>3.5일 초과</b> 시 내륙 철도 수송 비중 <b>30%</b> 확대")
    st.write(f"- <b>항만 체류시간 감축 연동</b>: 목표 절감 시간 <b>8.5시간/TEU</b> 반영")

    st.markdown("<b>4. 정량적 ROI 재무 내역 상세</b>", unsafe_allow_html=True)
    st.write(f"- <b>총 분석 물동량</b>: {total_teu:,} TEU (voyages {len(df_voyages):,}건 연동)")
    st.write(f"- <b>시간당 기회손실 단가</b>: ${avg_freight / 24.0:.2f} / hr/TEU")
    st.write(f"- <b>총 지연 손실 방지액 (Savings)</b>: ${total_savings:,.2f}")
    st.write(f"- <b>총 전략 집행 비용 (Cost)</b>: ${total_cost:,.2f}")
    st.write(f"- <b>최종 순 재무적 이익 (Net Benefit)</b>: ${net_benefit:,.0f}")
else:
  st.warning(
      "👈 좌측 사이드바에 1. 글로벌 운송 파일(voyages)을 업로드해 주세요. 통합 데이터셋(4Tabs)은 자동으로 인식됩니다."
  )
