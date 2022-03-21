import os
import json
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config import MEALS_URL


# 학교 정보
df = pd.read_csv("data/school_info_with_codes.csv")
school_info_with_codes = df.loc[~df['school_code'].isnull()]

# API Key
neis_key = os.environ['NEIS_KEY']

# 급식 정보 저장
more_data = {}
error_data = {}
for idx, row in school_info_with_codes.iterrows():
    province_code = row['province_code']
    school_code = row['school_code']
    school_name = row['school_name']

    payload = {
        'KEY': neis_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 1000,
        'ATPT_OFCDC_SC_CODE': province_code,
        'SD_SCHUL_CODE': school_code
    }
    
    try:
        resp = requests.get(MEALS_URL, params=payload)
        data = resp.json()

        total_page = data['mealServiceDietInfo'][0]['head'][0]['list_total_count']

        # 전체 페이지가 1000페이지 이상이면 다른 처리 필요
        if total_page > 1000:
            more_data[school_code] = province_code

    # 에러 발생 시
    except Exception as e:
        error_data[school_code] = province_code

# 1000건보다 많은 데이터가 있을 경우
temp = []
for school_code, sido_code in more_data.items():
    payload = {
        'KEY': neis_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 1000,
        'ATPT_OFCDC_SC_CODE': sido_code,
        'SD_SCHUL_CODE': school_code
    }
    
    resp = requests.get(MEALS_URL, params=payload)
    data = resp.json()

    total_count = data['mealServiceDietInfo'][0]['head'][0]['list_total_count']
    temp.append({
        'sido_code': sido_code,
        'school_code': school_code,
        'school_name': data['mealServiceDietInfo'][-1]['row'][0]['SCHUL_NM'],
        'page_number': total_count // 1000 + 1       
    })

# 1000건 보다 많은 경우만 다시 크롤링
more_data_df = pd.DataFrame(temp)
for idx, row in more_data_df[363:].iterrows():
    sido_code = row['sido_code']
    school_code = row['school_code']
    school_name = row['school_name']
    total_page = row['page_number']
    
    result = []
    page = 1
    while page <= total_page:
        payload = {
            'KEY': neis_key,
            'Type': 'json',
            'pIndex': page,
            'pSize': 1000,
            'ATPT_OFCDC_SC_CODE': sido_code,
            'SD_SCHUL_CODE': school_code
        }
        
        try:
            resp = requests.get(MEALS_URL, params=payload)
            data = resp.json()
            rows = data['mealServiceDietInfo'][-1]['row']
        except Exception as e:
            page = total_page + 1
            continue

        result.extend(rows)
    
        page += 1
        
    df = pd.DataFrame(result)
    df.columns = ['시도교육청코드', '시도교육청명', '표준학교코드', '학교명', \
                  '식사코드', '식사명', '급식일자', '급식인원수', '요리명', \
                  '원산지정보', '칼로리정보', '영양정보', '급식시작일자', '급식종료일자']
    df.to_csv(f'./meals/{school_name}.csv', index=False)