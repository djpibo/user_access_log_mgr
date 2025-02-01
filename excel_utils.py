import pandas as pd
import openpyxl
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)


def get_excel_sheets(file) -> list:
    """
    업로드된 엑셀 파일의 시트 목록을 반환합니다.
    """
    if file is None:
        logging.warning("⚠ 파일이 업로드되지 않았습니다.")
        return []

    try:
        xls = pd.ExcelFile(file, engine="openpyxl")
        sheet_names = xls.sheet_names

        if not sheet_names:
            logging.warning("⚠ 시트가 없는 엑셀 파일입니다.")
            return []

        return sheet_names

    except Exception as e:
        logging.error(f"🚨 시트 목록을 가져오는 중 오류 발생: {e}")
        return []


def read_excel_sheet(file, sheet_name: str) -> pd.DataFrame:
    """
    특정 시트의 데이터를 Pandas DataFrame으로 변환합니다.
    """
    if file is None or not sheet_name:
        logging.warning("⚠ 파일 또는 시트 이름이 제공되지 않았습니다.")
        return pd.DataFrame()

    try:
        df = pd.read_excel(file, sheet_name=sheet_name, engine="openpyxl")

        if df.empty:
            logging.warning(f"⚠ 선택한 시트 '{sheet_name}'에 데이터가 없습니다.")
            return pd.DataFrame()

        return df

    except Exception as e:
        logging.error(f"🚨 엑셀 시트 읽기 오류: {e}")
        return pd.DataFrame()


def get_column_names(df: pd.DataFrame) -> list:
    """
    데이터프레임의 컬럼명을 리스트로 반환합니다.
    """
    if df.empty:
        logging.warning("⚠ 데이터프레임이 비어 있어 컬럼을 반환할 수 없습니다.")
        return []

    return df.columns.tolist()


def convert_to_records(df: pd.DataFrame) -> list[dict]:
    """
    DataFrame을 Supabase에 삽입할 수 있도록 JSON 형식으로 변환합니다.
    """
    if df.empty:
        logging.warning("⚠ 변환할 데이터가 없습니다.")
        return []

    return df.to_dict(orient="records")
