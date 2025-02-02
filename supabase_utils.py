import logging
from supabase import create_client, Client

# Supabase 연결 설정
SUPABASE_URL = "https://sgymfpbnlbqeelbfiguc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNneW1mcGJubGJxZWVsYmZpZ3VjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNDgyODQsImV4cCI6MjA1MDkyNDI4NH0.1TriuQfF99YycEgGowmiZskXWX08dMzyIpn9bOeswsM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
bucket_name = "excel-files"  # Supabase Storage의 버킷 이름
logging.basicConfig(level=logging.INFO)

def create_table(table_name: str, columns: list[str]) -> bool:
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

        response = supabase.rpc("execute_sql", {"sql": create_table_query}, ).execute()

        if response.data is None:
            logging.error(f"🚨 테이블 생성 오류: {response.data}")
            return False
        else:
            logging.info(f"✅ 테이블 '{table_name}' 생성 완료")
            return True

    except Exception as e:
        logging.error(f"🚨 테이블 생성 중 오류 발생: {e}")
        return False

def insert_data(table_name: str, data: list[dict]) -> bool:

    try:
        if not data:
            logging.warning("⚠️ 삽입할 데이터가 없습니다.")
            return False

        # 모든 값을 문자열(TEXT)로 변환
        formatted_data = [{k: str(v) for k, v in row.items()} for row in data]

        response = supabase.table(table_name).insert(formatted_data).execute()

        if response.data is None:
            logging.error(f"🚨 테이블 생성 오류: {response.data}")
            return False
        else:
            logging.info(f"✅ 테이블 '{table_name}' 생성 완료")
            return True

    except Exception as e:
        logging.error(f"🚨 데이터 삽입 중 오류 발생: {e}")
        return False

def upload_to_supabase(file, file_name):
    file_content = file.read()
    supabase.storage.from_(bucket_name).upload(file_name, file_content, {"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
    return f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{file_name}"
