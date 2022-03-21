import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config import NEIS_SCHOOL_CODES_URL, EXCEL_DOWNLOAD_PATH

# 학교 이름, 학교 코드
df = pd.read_csv("data/school_info.csv", indef=False)

# NEIS 학교 급식 정보 엑셀 미리보기 다운로드
for idx, row in df.iterrows():
        
    school_name, sido_code = row['school_name'], row['province']
    driver = webdriver.Chrome('./chromedriver') # chrome driver path

    # excel 페이지 접속
    driver.get(NEIS_SCHOOL_CODES_URL)

    # 시도 선택
    select_sido = Select(driver.find_element_by_id('sheet-filter-ATPT_OFCDC_SC_CODE'))
    select_sido.select_by_value(sido_code)
    
    # 학교 이름 입력
    name_input = driver.find_element_by_id('sheet-filter-SCHUL_NM')
    name_input.send_keys(school_name)

    # 검색 버튼 클릭
    click_button = driver.find_element_by_id('sheet-search-button')
    click_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'SheetObject')))
    
    # 다운로드 버튼 클릭 후 엑셀 파일 저장
    download_button = driver.find_element_by_id('sheet-csv-button')
    download_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    time.sleep(3)
    driver.switch_to.alert.accept()
    time.sleep(3)
    driver.close()

# 학교 코드 채우기
code_dict = {}
error_files = []
files = os.listdir(EXCEL_DOWNLOAD_PATH)
for file in files:
    if '급식식단정보' in file:
        file_path = f"{EXCEL_DOWNLOAD_PATH}/{file}"
        try:
            # 엑셀 파일 열기
            data = pd.read_csv(file_path)

            # 학교 이름, 학교 코드 추출
            school_name, school_code = data['학교명'].unique()[0], data['표준학교코드'].unique()[0]
            code_dict[school_name] = str(school_code)
            del data
        except Exception as e:
            error_files.append(file_path)
            continue

# 학교 이름별 학교 코드 매칭
df['school_code'] = df['school_name'].map(code_dict)

# 데이터 저장
df.to_csv("data/school_info_with_codes.csv", index=False)
            