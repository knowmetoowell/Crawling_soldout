#%%
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# SoldOut Web Scraping(crawling)

# https://www.soldout.co.kr/trade/detail/15662    -> 신발 15885개
# https://www.soldout.co.kr/trade/detail/21193    -> 시계 55개

url = "https://www.soldout.co.kr/trade/detail/15662" # 찾고싶은 신발 URL 입력
num_of_scroll = 0
# 스크롤 횟수 지정
# 한번 스크롤 당 데이터 50개 늘어남
# 0 입력 시 데이터 끝날 때 까지 스크롤함
# ex) num_of_scroll = 10 인 경우 총 데이터 550개
# 구분해놓은 이유: num_of_scroll을 지정하는 게 데이터 검색을 덜 해서 더 빠르긴 함
ID = '********'
PW = '********'


chrome_options = Options()
chrome_options.add_argument("disable-gpu")   # 가속 사용 x
chrome_options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
driver = webdriver.Chrome(chrome_options=chrome_options)
# 크롬 드라이버 설치 해야함.
# 1. https://chromedriver.chromium.org/downloads 접속
# 2. 본인 크롬 버전에 맞는 크롬 드라이버 선택
# 3. 본인 크롬 버전 확인 방법
#   - 크롬 -> 더보기(우상단 세로 점 세개) -> 도움말 -> Chrome 정보(G)
# 4. win32.zip 다운로드 -> window os 사용할 경우
# 5. chromedriver.exe 파일을 .py 파일과 같은 디렉토리에 위치
#   - 같은 위치에 놓지 않는 경우
#   - driver = webdriver.Chrome('C:\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options)
#   - 이런식으로 경로 지정해주면 됨.


# 자동 로그인
driver.get('https://www.soldout.co.kr/member/login')
driver.implicitly_wait(3)
login_xpath='//*[@id="__layout"]/div/div[2]/div/form/button'
id_xpath = '//*[@id="__layout"]/div/div[2]/div/form/div[1]/div/input'
pw_xpath='//*[@id="__layout"]/div/div[2]/div/form/div[2]/div/input'


driver.find_element(By.XPATH, id_xpath).send_keys(ID)
time.sleep(1)
driver.find_element(By.XPATH, pw_xpath).send_keys(PW)
time.sleep(1)
driver.find_element(By.XPATH, login_xpath).click()
time.sleep(1)





## 크롤링 시작
driver.get(url)
time.sleep(1)
driver.find_element(By.CLASS_NAME, 'btn-show-all').click() # 전체보기 클릭
time.sleep(1)

# 무한 스크롤 구현
elem = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/table/tbody')
count = 0
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')
tbody_target = soup.select("body > div.BaseModal.trade_modal > div > div > div.base-table.trade_modal__table.modal-table > table > tbody")
trData = tbody_target[0].find_all('tr')
last_tr_cnt = len(trData)

while True: # 무한 스크롤
    driver.execute_script("arguments[0].scrollBy(0, document.body.scrollHeight)", elem)
    time.sleep(0.5) # 최소 0.5초 이상 줘야 데이터 읽어옮

    count+=1
    if num_of_scroll <= 0:
        if count % 20 == 0: # 20번 스크롤할 때마다 한번 씩 데이터양 체크함
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            tbody_target = soup.select("body > div.BaseModal.trade_modal > div > div > div.base-table.trade_modal__table.modal-table > table > tbody")
            trData = tbody_target[0].find_all('tr')
            next_tr_cnt = len(trData)
            if next_tr_cnt == last_tr_cnt:
                break
            else:
                print("현재 데이터 양: ",next_tr_cnt)
                last_tr_cnt = next_tr_cnt
    else:
        if num_of_scroll == count:
            break



print("검색된 데이터 양: ", last_tr_cnt)


html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')


tbody_target = soup.select("body > div.BaseModal.trade_modal > div > div > div.base-table.trade_modal__table.modal-table > table > tbody")
trData = tbody_target[0].find_all('tr')
tdData = trData[0].find_all('td')

columnList = []
rowList = []

for i in range(len(trData)):
    tdData = trData[i].find_all('td')
    #print(tdData)

    for j in range(len(tdData)):
        element = tdData[j].text.replace('\n', '').strip()
        columnList.append(element)

    rowList.append(columnList)
    columnList = []


df = pd.DataFrame(rowList, columns=['날짜', '사이즈', '가격'])
print(df)
df.to_csv("./result.csv", encoding='utf-8-sig')

