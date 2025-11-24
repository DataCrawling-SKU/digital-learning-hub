import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

if 'selected_center' not in st.session_state:
  st.session_state.selected_center = None

st.title("디지털 배움터 찾기")
st.markdown("---")

#지역 목록 가져오기
def get_regions():
  response = requests.get(f'{API_URL}/api/regions')
  return response.json()["regions"]

# 교육자 지원 화면
def apply_form(center):
  st.header(f"교육자 지원서 작성")
  st.info(f"**{center['배움터명']}** 교육자 모집")

  with st.form("application_form"):
    st.markdown("### 기본 정보")
    name = st.text_input("이름 *", placeholder="김서경")
    phone = st.text_input("연락처 *", placeholder="010-1234-5678")

    st.markdown("### 기타 정보")
    major = st.text_input("학과 *", placeholder="소프트웨어학과")
    teach_category = st.multiselect(
      "가능한 교육분야(복수 선택 가능)",
      ["복지/건강", "세금/재정", "행정/법률", "취업/경제", "교육/청소년","교통", "부동산/토지", "전자정부플랫폼"]
    )

    st.markdown("### 지원동기")
    motivation = st.text_area("지원 동기 및 자기소개", height=150)

    # 제출 버튼
    col1, col2 = st.columns([1,1])
    with col1:
      submitted = st.form_submit_button("제출", use_container_width=True)
    with col2:
      if st.form_submit_button("처음으로", use_container_width=True):
        st.session_state.selected_center = None
        st.rerun()

    if submitted:
      if name and phone and major and teach_category and motivation:
        st.success("지원서가 제출되었습니다!")
      else:
        st.error("입력하지 않은 항목이 있습니다.")

# 메인 화면
if st.session_state.selected_center is None:
  regions = get_regions()
  selected_region = st.selectbox("지역을 선택하세요", [""] + regions, index=0)

  if selected_region:
    response = requests.get(f'{API_URL}/api/centers/{selected_region}')
    data = response.json()
  
    if data["count"] > 0:
      st.success(f"**{data['region']}**에 총 **{data['count']}개**의 배움터가 있습니다")

      for idx, center in enumerate(data["centers"]):
        col1, col2 = st.columns([4,1])

        with col1:
          st.markdown(f"""
                        <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #667eea;">
                            <h3 style="color: black;">{center['배움터명']}</h3>
                            <p style="color: black;"><strong>주소:</strong> {center['배움터주소']}</p>
                            <p style="color: black;"><strong>유형:</strong> {center['배움터 유형']} | <strong>정원:</strong> {center['이용정원']}명</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        with col2:
          st.write("")  # 위치 조정용
          if st.button("교육자 지원 →", key=f"apply_{idx}", use_container_width=True):
            st.session_state.selected_center = center
            st.rerun()
    else:
      st.warning("해당 지역에는 배움터가 없습니다.")
else:
  apply_form(st.session_state.selected_center)