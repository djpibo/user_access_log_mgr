import pandas as pd
from supabase import Client
import logging

logging.basicConfig(level=logging.INFO)  # 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
def create_table_if_not_exists(supabase: Client, df, table_name):

    df = df.iloc[:, :50]
    
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
        logging.error(f"❌ 테이블 생성 오류: {e}")
        return False

def insert_data_into_supabase(supabase: Client, df, table_name):
    df = df.where(pd.notna(df), None)
    data = df.to_dict(orient="records")  # JSON 변환

    try:
        response = supabase.table(table_name).insert(data, count="exact").execute()
        logging.info(f"✅ 데이터가 `{table_name}` 테이블에 저장되었습니다!")
        return response
    except Exception as e:
        logging.error(f"❌ 데이터 삽입 오류: {e}")
        return None
