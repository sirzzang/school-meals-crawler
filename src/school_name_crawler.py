# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from src.config import SCHOOL_INFO_URL


# 전국 학교 정보 지역 코드
with open('resources/province.json', 'r', encoding="UTF-8") as file:
    province_codes = json.load(file)

# neis API 지역 코드
with open('resources/province_edu.json', 'r', encoding="UTF-8") as file:
    province_edu_codes = json.load(file)

# 시도별 학교 이름
schools = []
for province, code in province_codes.items():

    req = requests.get(
        url=SCHOOL_INFO_URL,
        params={
            'PROVINCE_CODE': code
        }, 
        verify=False
    )

    resp = req.text
    soup = BeautifulSoup(resp, 'lxml')
    list_tags = soup.find_all("ul", class_="link_list")
    for tag in list_tags:
        school_tags = tag.find_all("li")
        for school in school_tags:
            schools.append([school.text, province])

# 학교 이름, neis 지역 코드 저장
df = pd.DataFrame(schools, columns=['school_name', 'province'])
df['province_code'] = df['province'].province_edu_codes

# 데이터 저장
df.to_csv("data/school_info.csv", indef=False)