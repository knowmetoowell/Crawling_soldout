# Crawling_soldout

# num_of_scroll = 0
스크롤 횟수 지정
한번 스크롤 당 데이터 50개 늘어남
0 입력 시 데이터 끝날 때 까지 스크롤함
ex) num_of_scroll = 10 인 경우 총 데이터 550개
구분해놓은 이유: num_of_scroll을 지정하는 게 데이터 검색을 덜 해서 더 빠르긴 함



# 크롬 드라이버 설치 해야함.
1. https://chromedriver.chromium.org/downloads 접속
2. 본인 크롬 버전에 맞는 크롬 드라이버 선택
3. 본인 크롬 버전 확인 방법
  - 크롬 -> 더보기(우상단 세로 점 세개) -> 도움말 -> Chrome 정보(G)
4. win32.zip 다운로드 -> window os 사용할 경우
5. chromedriver.exe 파일을 .py 파일과 같은 디렉토리에 위치
  - 같은 위치에 놓지 않는 경우
  - driver = webdriver.Chrome('C:\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options)
  - 이런식으로 경로 지정해주면 됨.
