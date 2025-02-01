import logging
from supabase import create_client, Client

# Supabase 연결 설정
SUPABASE_URL = "https://sgymfpbnlbqeelbfiguc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNneW1mcGJubGJxZWVsYmZpZ3VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNDgyODQsImV4cCI6MjA1MDkyNDI4NH0.1TriuQfF99YycEgGowmiZskXWX08dMzyIpn9bOeswsM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
logging.basicConfig(level=logging.INFO)

def create_table(table_name: str, columns: list[str]) -> bool:
    """
    Supabase에 새로운 테이블을 생성합니다. 모든 컬럼을 TEXT 타입으로 설정하여 타입 호환성을 보장합니다.
    """
    try:
        if not columns:
            logging.error("🚨 컬럼 목록이 비어 있습니다.")
            return False

        column_definitions = ", ".join([f'"{col}" TEXT' for col in columns])

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            {column_definitions},
            created_at TIMESTAMP DEFAULT now()
        );
        """
        response = supabase.rpc("execute_sql", {"sql": create_table_query}).execute()

        if response.error:
            logging.error(f"🚨 테이블 생성 오류: {response.error}")
            return False

        logging.info(f"✅ 테이블 '{table_name}' 생성 완료")
        return True

    except Exception as e:
        logging.error(f"🚨 테이블 생성 중 오류 발생: {e}")
        return False


def insert_data(table_name: str, data: list[dict]) -> bool:
    """
    Supabase 테이블에 데이터를 삽입합니다.
    모든 데이터는 TEXT 형식으로 변환 후 저장됩니다.
    """
    try:
        if not data:
            logging.warning("⚠️ 삽입할 데이터가 없습니다.")
            return False

        # 모든 값을 문자열(TEXT)로 변환
        formatted_data = [{k: str(v) for k, v in row.items()} for row in data]

        response = supabase.table(table_name).insert(formatted_data).execute()

        if response.error:
            logging.error(f"🚨 데이터 삽입 오류: {response.error}")
            return False

        logging.info(f"✅ 데이터 삽입 완료 ({len(data)} rows)")
        return True

    except Exception as e:
        logging.error(f"🚨 데이터 삽입 중 오류 발생: {e}")
        return False