import requests
import pandas as pd
import os

# 한국지능정보사회진흥원 디지털배움터 교육장 현황 api url
API_URL = 'https://api.odcloud.kr/api/15134509/v1/uddi:7172b895-8193-44c1-a3c7-c52322104653'
API_KEY = '0VGmzq6hyxxRhjYc0ZS1Fq2tHHoBnbBYMKCMbDKtnebtUS44dvI%2B0GuldwLIW3nk7d4rqcxFsPss9Fm6RQlWRQ%3D%3D'
SERVICE_KEY = '0VGmzq6hyxxRhjYc0ZS1Fq2tHHoBnbBYMKCMbDKtnebtUS44dvI+0GuldwLIW3nk7d4rqcxFsPss9Fm6RQlWRQ=='

def call_all_data():
    all_data = []
    page = 1
    per_page = 100

    while True:
        params = {
            'page': page,
            'perPage': per_page,
            'serviceKey': SERVICE_KEY
        }

        headers = {
            'Authorization': API_KEY
        }

        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()

        data = result.get('data', [])
        if not data:
            break

        all_data.extend(data)

        if len(all_data) >= result.get('totalCount', 0):
            break

        page += 1

    return all_data

def create_csv():

    data = call_all_data()

    if not data:
        print("데이터가 없습니다")
        return

    df = pd.DataFrame(data)

    columns = ['관리지역', '배움터 유형', '배움터명', '배움터주소', '시군구', '이용정원']
    df = df[columns]

    # CSV 파일로 저장
    output_dir = '/Users/parkjuyong/Desktop/4-1/data-crawling-project/data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'digital_learning_centers.csv')

    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    # 확인용 출력
    print(df.head().to_string())

    return output_path

if __name__ == "__main__":
    create_csv()
