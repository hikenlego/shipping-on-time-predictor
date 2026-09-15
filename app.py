import pandas as pd
import streamlit as st
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor

st.set_page_config(
    page_title="해상 정시성 예측 시스템", page_icon="🚢", layout="wide"
)

st.title("🚢 해상 정시성 및 지연시간 예측 시스템")
st.markdown(
    "엑셀(.xlsx, .xls) 또는 CSV 파일을 업로드하면 XGBoost 모델이 예측 결과를"
    " 도출합니다."
)

# Sidebar: 엑셀 및 CSV 파일 모두 지원
uploaded_file = st.sidebar.file_uploader(
    "엑셀 또는 CSV 파일을 선택하세요", type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
  # 파일 확장자에 따른 데이터 읽기
  file_name = uploaded_file.name
  if file_name.endswith(".csv"):
    data = pd.read_csv(uploaded_file)
  else:
    data = pd.read_excel(uploaded_file)

  st.subheader("📋 입력 데이터 미리보기")
  st.dataframe(data.head(5))

  if st.button("🚀 예측 모델 학습 및 결과 생성"):
    with st.spinner("모델 학습 중..."):
      X = data.drop(columns=["actual_delay_hours", "on_time_target"])
      y_reg = data["actual_delay_hours"]
      y_cls = data["on_time_target"]

      for col in X.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

      X_train, X_test, y_reg_train, y_reg_test, y_cls_train, y_cls_test = (
          train_test_split(
              X, y_reg, y_cls, test_size=0.2, random_state=42
          )
      )

      cls_model = XGBClassifier(n_estimators=100, max_depth=5, random_state=42)
      cls_model.fit(X_train, y_cls_train)

      reg_model = XGBRegressor(n_estimators=100, max_depth=5, random_state=42)
      reg_model.fit(X_train, y_reg_train)

      cls_pred = cls_model.predict(X_test)
      reg_pred = reg_model.predict(X_test)

      col1, col2, col3 = st.columns(3)
      col1.metric(
          "정시성 정확도",
          f"{accuracy_score(y_cls_test, cls_pred) * 100:.2f}%",
      )
      col2.metric(
          "평균 오차 (MAE)",
          f"{mean_absolute_error(y_reg_test, reg_pred):.2f} 시간",
      )
      col3.metric("결정계수 (R²)", f"{r2_score(y_reg_test, reg_pred):.4f}")

      st.success("예측이 완료되었습니다!")
else:
  st.info("좌측 사이드바에서 엑셀 또는 CSV 파일을 업로드해 주세요.")
