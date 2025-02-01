import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os

# Supabase 연결 설정
SUPABASE_URL = "https://sgymfpbnlbqeelbfiguc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNneW1mcGJubGJxZWVsYmZpZ3VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNDgyODQsImV4cCI6MjA1MDkyNDI4NH0.1TriuQfF99YycEgGowmiZskXWX08dMzyIpn9bOeswsM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit UI 설정
st.title("📂 엑셀 업로드 및 Supabase 저장")
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

# 테이블명 입력
table_name = st.text_input("Supabase 테이블 이름 입력", "uploaded_excel_data")

if uploaded_file and table_name:
    # 엑셀 데이터 읽기
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    if st.button("Supabase에 저장하기"):
        try:
            # 첫 번째 줄을 컬럼명으로 사용
            columns = df.columns.tolist()

            # Supabase 테이블 생성 (CREATE TABLE)
            column_definitions = ", ".join([f'"{col}" TEXT' for col in columns])
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                {column_definitions},
                created_at TIMESTAMP DEFAULT now()
            );
            """

            # SQL 실행
            response = supabase.rpc("execute_sql", {"sql": create_table_query}).execute()

            if response.error:
                st.error(f"🚨 테이블 생성 오류: {response.error}")
            else:
                st.success(f"✅ 테이블 '{table_name}' 생성 완료!")

            # 데이터 삽입
            data = df.to_dict(orient="records")
            insert_response = supabase.table(table_name).insert(data).execute()

            if insert_response.error:
                st.error(f"🚨 데이터 삽입 오류: {insert_response.error}")
            else:
                st.success(f"✅ 데이터 삽입 완료 ({len(data)} rows)")

        except Exception as e:
            st.error(f"🚨 오류 발생: {e}")

# 데이터 미리보기
if uploaded_file:
    st.subheader("📊 엑셀 데이터 미리보기")
    st.dataframe(df.head(10))
