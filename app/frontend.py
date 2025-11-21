import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("디지털 배움터 찾기")
st.markdown("---")

#지역 목록 가져오기
def get_regions():
  response = requests.get(f'{API_URL}/api/regions')
  return response.json()["regions"]

regions = get_regions()
selected_region = st.selectbox("지역을 선택하세요", [""] + regions, index=0)

if selected_region:
  response = requests.get(f'{API_URL}/api/centers/{selected_region}')
  data = response.json()
  
  if data["count"] > 0:
    st.success(f"**{data['region']}**에 총 **{data['count']}개**의 배움터가 있습니다")

    for center in data["centers"]:
      with st.container():
        st.markdown(f"""
                    <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #667eea;">
                        <h3 style="color: black;">{center['배움터명']}</h3>
                        <p style="color: black;"><strong>주소:</strong> {center['배움터주소']}</p>
                        <p style="color: black;"><strong>유형:</strong> {center['배움터 유형']} | <strong>정원:</strong> {center['이용정원']}명</p>
                    </div>
                """, unsafe_allow_html=True)
  else:
    st.warning("해당 지역에는 배움터가 없습니다.")