import streamlit as st
from excel_utils import read_excel, get_column_names, convert_to_records
from supabase_utils import create_table, insert_data

# Streamlit UI 설정
st.title("📂 엑셀 업로드 및 Supabase 저장")
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

# 테이블명 입력
table_name = st.text_input("Supabase 테이블 이름 입력", "uploaded_excel_data")

if uploaded_file and table_name:
    df = read_excel(uploaded_file)

    if not df.empty:
        st.subheader("📊 엑셀 데이터 미리보기")
        st.dataframe(df.head(10))

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
