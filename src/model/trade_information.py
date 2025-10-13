from dto.trade_information_creation_request import TradeInformationCreationRequest


class TradeInformation:
    """개별 종목의 거래 정보를 담는 데이터 클래스"""

    def __init__(self):
        self.name: str = ""
        self.ticker: str = ""
        self.price: int = 0
        self.change: int = 0
        self.change_rate: float = 0.0
        self.volume: int = 0
        self.value: int = 0
        self.market_cap: int = 0

    def __repr__(self) -> str:
        return (f"TradeInformation(name='{self.name}', ticker='{self.ticker}', price={self.price}, "
                f"change={self.change}, change_rate={self.change_rate}%, volume={self.volume}, "
                f"value={self.value}, market_cap={self.market_cap})")

    def toTradeInformationCreationRequest(self) -> TradeInformationCreationRequest:
        """TradeInformation 객체를 API 전송용 DTO로 변환"""
        dto = TradeInformationCreationRequest()
        dto.name = self.name
        dto.ticker = self.ticker
        dto.price = self.price
        dto.volume = self.volume
        dto.value = self.value
        dto.marketCap = self.market_cap
        return dto
