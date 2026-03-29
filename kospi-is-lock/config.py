class Config:
    TELEGRAM_TOKEN = ''
    CHAT_ID = ''
    VWAP_PERIOD = 20     # 20일 VWAP 기준
    LOOKBACK_DAYS = 60   # VWAP 계산을 위해 수집할 과거 데이터 일수
    TOP_N = 200          # 분석할 시가총액 상위 종목 개수

class KisConfig:
    """한국투자증권 OpenAPI 접속을 위한 설정"""
    APP_KEY = ''             # 한국투자증권 OpenAPI 발급 App Key (따옴표 안에 입력)
    APP_SECRET = ''          # 한국투자증권 OpenAPI 발급 App Secret (따옴표 안에 입력)
    ACCOUNT = '00000000-01'  # 예: 12345678-01 (자신 종합계좌 8자리 - 두자리 끝자리)
    IS_MOCK = True           # 모의투자 우선
