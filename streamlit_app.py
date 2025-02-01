import streamlit as st
from excel_utils import get_excel_sheets, read_excel_sheet, get_column_names, convert_to_records
from supabase_utils import create_table, insert_data

# Streamlit UI 설정
st.title("EXCEL UPLOAD")

# 📂 엑셀 파일 업로드
uploaded_file = st.file_uploader("STEP 1) 엑셀 파일을 업로드", type=["xlsx"])

if uploaded_file:
    # ✅ 엑셀 시트 목록 가져오기
    excel_sheets = get_excel_sheets(uploaded_file)

    if not excel_sheets:
        st.error("🚨 유효한 시트가 없습니다. 올바른 엑셀 파일을 업로드하세요.")
        st.stop()

    # 📑 사용자가 시트 선택
    selected_sheet = st.selectbox("STEP 2) 시트 선택", excel_sheets)

    if selected_sheet:
        # ✅ 선택한 시트 데이터 불러오기
        df = read_excel_sheet(uploaded_file, selected_sheet)

        if df.empty:
            st.error(f"🚨 '{selected_sheet}' 시트에 데이터가 없습니다.")
            st.stop()

        # 🔍 예상 컬럼명 미리보기
        st.write("")
        st.subheader("HEADER COLUMN")
        st.write(df.head(1))  # 첫 줄 미리보기

        # 🔠 Supabase 테이블명 입력 (기본값: 시트 이름)
        default_table_name = selected_sheet.replace(" ", "_").lower()
        table_name = st.text_input("STEP 3) 테이블명 입력", default_table_name)

        if st.button("DB INSERT"):
            columns = get_column_names(df)

            if not columns:
                st.error("🚨 유효한 컬럼이 없습니다.")
                st.stop()

            with st.spinner("⏳ 테이블 생성 중..."):
                if create_table(table_name, columns):
                    st.success(f"✅ 테이블 '{table_name}' 생성 완료!")
                else:
                    st.error("🚨 테이블 생성 오류 발생")
                    st.stop()

            with st.spinner("⏳ 데이터 삽입 중..."):
                data = convert_to_records(df)
                if insert_data(table_name, data):
                    st.success(f"✅ 데이터 삽입 완료 ({len(data)} rows)")
                else:
                    st.error("🚨 데이터 삽입 오류 발생")
