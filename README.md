# school-meals-crawler

> 나이스 교육정보 개방 포털에서 전국 학교 급식식단정보 데이터셋을 얻을 수 있다.

급식식단정보 데이터셋에서 제공하는 급식식단정보 Open API를 이용해 전국 학교 급식 식단을 저장하는 ~~급하게 만든~~ 크롤러

## 개요

 나이스 교육정보 개방 포털에서는 [Open API](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=2)와 [sheet](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=1)를 통해 급식식단정보 데이터셋을 공개하고 있다.

* Open API 필수 신청 인자
  * 시도교육청코드(`ATPT_OFCDC_SC_CODE`)
  * 표준학교코드(`SD_SCHUL_CODE`)


Open API 이용 시 필수 신청 인자인 표준학교 코드는 나이스 교육정보 개방 포털에 공개되어 있지 않다. 한 학교의 식단을 알기 위해서는 Sheet을 이용해 시도교육청코드, 학교명을 입력한 뒤 급식일자를 검색하면 데이터를 다운로드할 수 있다.

## 크롤러 구성

1. `school_name_crawler`: [학교알리미 전국학교현황](https://www.schoolinfo.go.kr/ei/ss/pneiss_a08_s0.do)에서 전국의 초중고등학교 이름을 크롤링
2. `school_code_crawler`: [나이스 교육정보 개방 포털 급식식단정보 데이터셋 sheet]에서 전국 초중고등학교 이름 별로 교육청 지역, 학교 이름 선택 후 샘플 급식 식단 데이터셋 저장. 이후 학교별 샘플 급식 식단 데이터셋에서 학교 이름, 표준학교코드 추출
3. `meals_crawler.py`: 급식식단정보 Open API에 시도교육청코드, 표준학교코드 입력 후 식단 다운로드
