import streamlit as st
import pandas as pd
from supabase import create_client, Client
from handler.file_handler import upload_to_supabase, download_from_supabase
from handler.db_handler import create_table_if_not_exists, insert_data_into_supabase

# Supabase 연결 설정
SUPABASE_URL = "https://sgymfpbnlbqeelbfiguc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNneW1mcGJubGJxZWVsYmZpZ3VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNDgyODQsImV4cCI6MjA1MDkyNDI4NH0.1TriuQfF99YycEgGowmiZskXWX08dMzyIpn9bOeswsM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# S3용 client
SUPABASE_S3_KEY = "38c38450af2ddd3e4d9e47ee1a14415c"

supabase_s3: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit UI
st.title("📊 대용량 엑셀 파일 업로드 및 Supabase 저장")

# 파일 업로드
uploaded_file = st.file_uploader("📂 엑셀 파일을 업로드하세요", type=["xlsx", "csv"])

if uploaded_file:
    file_name = uploaded_file.name

    # 1️⃣ 파일 업로드 버튼
    with st.spinner("🔄 파일을 업로드하는 중..."):
        message, file_url = upload_to_supabase(supabase_s3, uploaded_file, file_name)
        st.info(message)
    
    # 2️⃣ 파일 다운로드 버튼
    with st.spinner("🔄 파일을 다운로드하는 중..."):
        file_path = download_from_supabase(supabase_s3, file_name)
        st.success(f"✅ 파일 다운로드 완료: {file_name}")

    # 3️⃣ 데이터 로드 및 미리보기 버튼
        with st.spinner("🔄 데이터를 로드하는 중..."):
            df = pd.read_excel(file_path) if file_name.endswith('.xlsx') else pd.read_csv(file_path)
            st.write("📊 업로드된 데이터 미리보기 (상위 3줄)")
            st.dataframe(df.head(3))

    # 4️⃣ Supabase에 테이블 생성 버튼
    default_table_name = file_name.split('.')[0]  # 확장자 제거한 파일명을 기본 테이블명으로 설정
    table_name = st.text_input("📌 테이블 이름을 설정하세요:", value=default_table_name)

    if st.button("🛠 테이블 생성"):
        with st.spinner("🔄 테이블을 생성하는 중..."):
            if create_table_if_not_exists(supabase, df):
                st.success("✅ 테이블 생성 완료!")

    # 5️⃣ 데이터 삽입 버튼
    if st.button("📥 데이터 삽입"):
        with st.spinner("🔄 Supabase에 데이터를 저장하는 중..."):
            insert_data_into_supabase(supabase, df)
