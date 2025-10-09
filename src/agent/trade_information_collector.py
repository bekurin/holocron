import re
import requests

from bs4 import BeautifulSoup
from util.string import clean_text
from typing import List
from model.trade_information import TradeInformation


class TradeInformationCollectorAgent:
    """KOSPI 100 종목의 기본 거래 정보를 수집하는 에이전트"""

    def __init__(self) -> None:
        self.name = "Trade Information Collector Agent"
        self.base_url = "https://finance.naver.com/sise/entryJongmok.naver"
        self.params = {"type": "KPI100"}
        self.trade_informations: List[TradeInformation] = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def _parse_page(self, html: str) -> List[TradeInformation]:
        """한 페이지의 HTML을 파싱하여 TradeInformation 리스트를 반환"""
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select('table.type_1 tr')

        page_results = []
        for row in rows:
            if not row.find('td', class_='ctg'):
                continue

            cols = row.find_all('td')
            change_span = cols[2].find('span', class_='tah')
            change_value_raw = clean_text(change_span.text)
            change_value = int(change_value_raw)

            if 'bu_pdn' in cols[2].find('em')['class']:
                change_value *= -1

            info = TradeInformation()
            info.name = cols[0].a.text
            info.ticker = re.search(r'code=(\d+)', cols[0].a['href']).group(1)
            info.price = int(clean_text(cols[1].text))
            info.change = change_value
            info.change_rate = float(clean_text(cols[3].text.replace('%', '')))
            info.volume = int(clean_text(cols[4].text))
            info.value = int(clean_text(cols[5].text))
            info.market_cap = int(clean_text(cols[6].text))

            page_results.append(info)

        return page_results

    def run(self) -> List[TradeInformation]:
        """1페이지부터 10페이지까지 순회하며 데이터 수집을 실행"""
        print(f"'{self.name}'이 KOSPI 100 정보 수집을 시작합니다.")

        for page in range(1, 11):
            self.params['page'] = page

            try:
                response = requests.get(
                    self.base_url, params=self.params, headers=self.headers)
                response.raise_for_status()
                page_data = self._parse_page(response.text)
                self.trade_informations.extend(page_data)
                print(f"  - {page}페이지 수집 완료. (수집된 종목 수: {len(page_data)}개)")

            except requests.exceptions.RequestException as e:
                print(f"오류: {page}페이지를 가져오는 데 실패했습니다. 에러: {e}")
                break

        print(f"총 {len(self.trade_informations)}개 종목의 정보 수집을 완료했습니다.")
        return self.trade_informations
