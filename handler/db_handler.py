import streamlit as st
import pandas as pd
from supabase import Client

table_name = "uploaded_data"

# Supabase에 테이블 존재 여부 확인 후 생성
def create_table_if_not_exists(supabase: Client, df):
    column_definitions = ", ".join([f'"{col}" TEXT' for col in df.columns])
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        {column_definitions}
    );
    """

    try:
        supabase.postgrest.rpc("execute_sql", {"sql": query}).execute()
        return True
    except Exception as e:
        st.error(f"❌ 테이블 생성 오류: {e}")
        return False

# Supabase에 데이터 삽입 (중복 방지)
def insert_data_into_supabase(supabase: Client, df):
    data = df.to_dict(orient="records")
    try:
        response = supabase.table(table_name).insert(data, count="exact").execute()
        st.success("✅ 데이터가 Supabase에 저장되었습니다!")
        return response
    except Exception as e:
        st.error(f"❌ 데이터 삽입 오류: {e}")
        return None
