from supabase import create_client, Client
import os

# Supabase 연결 설정
SUPABASE_URL = "https://sgymfpbnlbqeelbfiguc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNneW1mcGJubGJxZWVsYmZpZ3VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNDgyODQsImV4cCI6MjA1MDkyNDI4NH0.1TriuQfF99YycEgGowmiZskXWX08dMzyIpn9bOeswsM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_table(table_name: str, columns: list[str]) -> bool:
    """
    Supabase에 새로운 테이블을 생성합니다.
    """
    try:
        column_definitions = ", ".join([f'"{col}" TEXT' for col in columns])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            {column_definitions},
            created_at TIMESTAMP DEFAULT now()
        );
        """

        response = supabase.rpc("execute_sql", {"sql": create_table_query}).execute()
        return response.error is None
    except Exception as e:
        print(f"🚨 테이블 생성 오류: {e}")
        return False

def insert_data(table_name: str, data: list[dict]) -> bool:
    """
    Supabase 테이블에 데이터를 삽입합니다.
    """
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response.error is None
    except Exception as e:
        print(f"🚨 데이터 삽입 오류: {e}")
        return False
