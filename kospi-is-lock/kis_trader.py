import requests
import json

class KisTrader:
    """한국투자증권 OpenAPI 매수/매도 주문 통합 클래스"""
    def __init__(self, app_key, app_secret, account_number, is_mock=True):
        self.app_key = app_key
        self.app_secret = app_secret
        self.account_number = account_number # 예: "12345678-01"
        self.is_mock = is_mock
        
        # 실전투자 vs 모의투자 API 도메인 분리
        if self.is_mock:
            self.base_url = "https://openapivts.koreainvestment.com:29443"
        else:
            self.base_url = "https://openapi.koreainvestment.com:9443"
            
        self.access_token = self._issue_token()

    def _issue_token(self):
        """한국투자증권 OAuth 토큰 발급 (매일 리프레시 필요)"""
        if not self.app_key or not self.app_secret:
            return None
            
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        try:
            res = requests.post(url, headers=headers, data=json.dumps(payload))
            if res.status_code == 200:
                print("KIS API 토큰 발급 성공!")
                return res.json().get('access_token')
            else:
                print(f"KIS API 토큰 발급 실패: {res.text}")
                return None
        except Exception as e:
            print(f"KIS API 연결 오류: {e}")
            return None

    def order_market_buy(self, code, qty):
        """시장가 매수 (주문구분 01)"""
        return self._place_order(code, qty, is_buy=True, order_type="01", price=0)
        
    def order_market_sell(self, code, qty):
        """시장가 매도 (주문구분 01)"""
        return self._place_order(code, qty, is_buy=False, order_type="01", price=0)

    def _place_order(self, code, qty, is_buy, order_type, price):
        """공통 현금 매수/매도 주문 로직"""
        if not self.access_token:
            print(f"[모의 시뮬레이션] 종목:{code} | {qty}주 {'시장가 매수' if is_buy else '시장가 매도'} 실행 (API 키 미설정)")
            return None
            
        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/order-cash"
        
        # tr_id 결정을 위한 플래그 (V: 모의, T: 실전)
        real_prefix = "V" if self.is_mock else "T"
        action = "22" if is_buy else "21" # 22는 현금매수, 21은 현금매도
        tr_id = f"{real_prefix}TTC080{action}U"

        cano, prdt_cd = self.account_number.split("-")
        
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id
        }
        
        payload = {
            "CANO": cano,
            "ACNT_PRDT_CD": prdt_cd,
            "PDNO": code,           # 대상 종목 코드
            "ORD_DVSN": order_type, # 00: 지정가, 01: 시장가
            "ORD_QTY": str(qty),    # 주문 수량
            "ORD_UNPR": str(price)  # 주문 단가 (시장가는 0)
        }
        
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        result = res.json()
        print(f"주문 응답: {result['msg1']}")
        return result
