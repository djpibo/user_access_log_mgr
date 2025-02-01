import pandas as pd

def get_excel_sheets(file) -> list:
    """
    업로드된 엑셀 파일의 시트 목록을 반환합니다.
    """
    try:
        return pd.ExcelFile(file, engine="openpyxl").sheet_names
    except Exception as e:
        print(f"🚨 시트 목록 조회 오류: {e}")
        return []

def read_excel_sheet(file, sheet_name: str) -> pd.DataFrame:
    """
    특정 시트의 데이터를 Pandas DataFrame으로 변환합니다.
    """
    try:
        return pd.read_excel(file, sheet_name=sheet_name, engine="openpyxl")
    except Exception as e:
        print(f"🚨 엑셀 시트 읽기 오류: {e}")
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
