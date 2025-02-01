import pandas as pd

def read_excel(file) -> pd.DataFrame:
    """
    업로드된 엑셀 파일을 Pandas DataFrame으로 변환합니다.
    """
    try:
        df = pd.read_excel(file, engine="openpyxl")
        return df
    except Exception as e:
        print(f"🚨 엑셀 파일 읽기 오류: {e}")
        return pd.DataFrame()

def get_column_names(df: pd.DataFrame) -> list[str]:
    """
    데이터프레임의 컬럼명을 리스트로 반환합니다.
    """
    return df.columns.tolist()

def convert_to_records(df: pd.DataFrame) -> list[dict]:
    """
    DataFrame을 Supabase에 삽입할 수 있도록 JSON 형식으로 변환합니다.
    """
    return df.to_dict(orient="records")
