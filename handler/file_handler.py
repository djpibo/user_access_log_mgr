import tempfile
import os
import re
import unicodedata
from supabase import Client

bucket_name = "excel-files"

# 파일명 정리 함수 (한글 제거, 특수 문자 변환)
def clean_filename(filename):
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("utf-8")
    filename = filename.replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "", filename)
    return filename

# Supabase Storage에 파일 업로드
def upload_to_supabase(supabase, file, file_name):
    safe_filename = clean_filename(file_name)
    file_content = file.read()
    file_path = f"{bucket_name}/{safe_filename}"  # 파일 경로

    # 파일이 이미 존재하는지 확인
    files = supabase.storage.from_(bucket_name).list()
    file_names = [file['name'] for file in files]

    if safe_filename in file_names:
        public_url = supabase.storage.from_(bucket_name).get_public_url(safe_filename)
        return f"⚠️ 파일 `{safe_filename}` 이미 존재. 업로드 건너뜀.", public_url

    # 파일 업로드
    supabase.storage.from_(bucket_name).upload(safe_filename, file_content, {
        "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })

    # 업로드된 파일의 퍼블릭 URL 가져오기
    public_url = supabase.storage.from_(bucket_name).get_public_url(safe_filename)

    return f"✅ 파일 `{safe_filename}` 업로드 성공!", public_url

# Supabase Storage에서 파일 다운로드
def download_from_supabase(supabase: Client, file_name):
    response = supabase.storage.from_(bucket_name).download(file_name)
    temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
    with open(temp_file_path, "wb") as f:
        f.write(response)
    return temp_file_path
