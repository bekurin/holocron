import json
import requests
from dto.trade_information_creation_request import TradeInformationCreationRequest
from model.trade_information import TradeInformation  # 경로에 맞게 수정하세요


def save_trade_informations(base_url: str, trade_informations: list[TradeInformation]):
    """TradeInformation 리스트를 API 서버로 전송하는 함수"""
    headers = {
        "Content-Type": "application/json",
    }

    trade_information_creation_requests = [
        trade_info.toTradeInformationCreationRequest().__dict__
        for trade_info in trade_informations
    ]

    payload = {
        "tradeInformations": trade_information_creation_requests
    }

    url = f"{base_url}/v1/trade-informations"

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()
        print("Response:", response.json())
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
        print("Response:", response.text)
    except Exception as err:
        print(f"오류 발생: {err}")
