
import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_news(year, quarter=None):
    base_url = "https://search.naver.com/search.naver"
    query = "달러환율"
    
    # 분기 기간 설정
    start_dates = {
        1: f"{year}.01.01",
        2: f"{year}.04.01",
        3: f"{year}.07.01",
        4: f"{year}.10.01"
    }
    
    end_dates = {
        1: f"{year}.03.31",
        2: f"{year}.06.30",
        3: f"{year}.09.30",
        4: f"{year}.12.31"
    }
    
    if quarter:
        start_date = start_dates.get(quarter)
        end_date = end_dates.get(quarter)
    else:
        start_date = f"{year}.01.01"    #시작날짜와 끝날짜는 yyyy.mm.dd포맷으로 들어가야함
        end_date = f"{year}.12.31"

    # 날짜 포맷 변환
    start1 = start_date
    end1 = end_date
    start2 = start_date.replace(".", "") #기간설정에 들어갈 날짜는 yyyymmdd 포맷으로 들어가야함
    end2 = end_date.replace(".", "")

    # 뉴스 추출 및 페이지네이션
    all_news_items = []
    for page in range(1, 51):  # 최대 50 페이지까지 검색
        params = {
            'where': 'news',
            'query': query, #검색 키워드
            'sort': '2',  # 오래된 순으로 정렬 0:관련도순 1:최신순 2:오래된순
            'photo': '0',
            'field': '0',
            'pd': '3',
            'ds': start1,   #시작 날짜 설정
            'de': end1,     #끝 날짜 설정
            'docid': '',
            'related': '0',
            'mynews': '0',
            'office_type': '0',
            'office_section_code': '0',
            'news_office_checked': '',
            'nso': f'so:r,p:from{start2}to{end2}',#기간 설정
            'is_sug_officeid': '0',
            'office_category': '0',
            'service_area': '0',
            'start': (page - 1) * 10 + 1  # 페이지네이션
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error: Unable to fetch data (status code: {response.status_code})")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 뉴스 추출
        news_items = []
        for item in soup.find_all('div', class_='news_area'):
            title_tag = item.find('a', class_='news_tit')
            if title_tag:
                title = title_tag.get_text()
                link = title_tag['href']
                news_items.append({'title': title, 'link': link})
        
        if not news_items:
            break  # 더 이상 뉴스가 없으면 종료
        
        all_news_items.extend(news_items)
        
        time.sleep(1)  # 너무 자주 요청하지 않도록 잠시 대기

    # JSON 파일로 저장
    file_name = f"news_{year}_{quarter if quarter else 'full'}.json"
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(all_news_items, file, ensure_ascii=False, indent=4)
    
    print(f"Saved {len(all_news_items)} news items to {file_name}")

def get_year():
    while True:
        try:
            year = int(input("검색할 년도를 입력하세요 (1990년 1분기 이후부터 검색 가능): "))
            if year < 1990:
                print("1990년 1분기 이후부터 검색 가능합니다. 다시 입력해주세요.")
            else:
                return year
        except ValueError:
            print("잘못된 입력입니다. 년도는 숫자만 입력할 수 있습니다.")

def get_quarter():
    while True:
        quarter = input("연도 또는 분기를 입력하세요 (Q1-Q4, 생략시 연도 전체 검색): ").strip()
        if not quarter:
            return None
        if quarter.startswith('Q') and quarter[1:].isdigit():
            q = int(quarter[1:])
            if 1 <= q <= 4:
                return q
            else:
                print("잘못된 분기입니다. Q1-Q4 중에서 입력해주세요.")
        else:
            print("잘못된 입력입니다. 분기는 Q1-Q4 형식으로 입력해주세요.")

def main():
    year = get_year()
    quarter = get_quarter()
    fetch_news(year, quarter)

if __name__ == "__main__":
    main()
