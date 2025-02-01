import streamlit as st
from excel_utils import get_excel_sheets, read_excel_sheet, get_column_names, convert_to_records
from supabase_utils import create_table, insert_data

# Streamlit UI 설정
st.title("📂 엑셀 업로드 및 Supabase 저장")
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    # 엑셀 시트 목록 가져오기
    excel_sheets = get_excel_sheets(uploaded_file)
    selected_sheet = st.selectbox("📑 시트를 선택하세요", excel_sheets)

    if selected_sheet:
        # 선택한 시트의 데이터 불러오기
        df = read_excel_sheet(uploaded_file, selected_sheet)

        # 첫 번째 줄을 컬럼명으로 가정하여 미리보기
        st.subheader("🔍 예상 컬럼명")
        st.write(df.head(1))  # 첫 줄만 표시 (칼럼명 예측)

        # Supabase 테이블명 입력
        table_name = st.text_input("Supabase 테이블 이름 입력", selected_sheet.replace(" ", "_").lower())

        if st.button("Supabase에 저장하기"):
            columns = get_column_names(df)

            if create_table(table_name, columns):
                st.success(f"✅ 테이블 '{table_name}' 생성 완료!")

                data = convert_to_records(df)
                if insert_data(table_name, data):
                    st.success(f"✅ 데이터 삽입 완료 ({len(data)} rows)")
                else:
                    st.error("🚨 데이터 삽입 오류 발생")
            else:
                st.error("🚨 테이블 생성 오류 발생")

        # 데이터 미리보기
        st.subheader("📊 데이터 미리보기")
        st.dataframe(df.head(10))
