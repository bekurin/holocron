from datetime import datetime
from config import Config, KisConfig
from telegram_notifier import TelegramNotifier
from market_data_provider import MarketDataProvider
from vwap_analyzer import VWAPAnalyzer
from kis_trader import KisTrader

class VWAPBot:
    """위 클래스들을 조합하여 전체 프로세스를 관장하는 파사드(오케스트레이터) 클래스"""
    def __init__(self, config):
        self.config = config
        self.notifier = TelegramNotifier(config.TELEGRAM_TOKEN, config.CHAT_ID)
        self.data_provider = MarketDataProvider()
        self.analyzer = VWAPAnalyzer(config.VWAP_PERIOD)
        self.kis_trader = KisTrader(
            app_key=KisConfig.APP_KEY,
            app_secret=KisConfig.APP_SECRET,
            account_number=KisConfig.ACCOUNT,
            is_mock=KisConfig.IS_MOCK
        )

    def _generate_report_message(self, breakouts):
        today_str = datetime.today().strftime('%Y-%m-%d')
        msg = f"🚀 *{today_str} KOSPI 상위 {self.config.TOP_N} VWAP 상승 돌파 알림*\n"
        msg += f"({self.config.VWAP_PERIOD}일선 돌파 종목)\n\n"
        
        if not breakouts:
            msg += "오늘 발생한 매수(상승 돌파) 신호가 없습니다. 🐾\n"
        else:
            for s in breakouts:
                vol_emoji = "⚡" if s['vol_ratio'] > 200 else ""
                msg += f"▪️ *{s['name']}* ({s['code']})\n"
                msg += f"  종가: {int(s['price']):,}원 (VWAP: {int(s['vwap']):,}원)\n"
                msg += f"  이격도: {s['deviation']:.2f}% | 거래량 폭발: {s['vol_ratio']:.0f}% {vol_emoji}\n\n"
        return msg

    def run(self):
        print("오늘의 VWAP 돌파 종목 분석을 시작합니다... (VWAPBot 실행중)")
        top_stocks = self.data_provider.get_kospi_top_n(self.config.TOP_N)
        
        breakout_stocks = []
        for stock in top_stocks:
            try:
                # 1. 데이터 가져오기
                df = self.data_provider.get_historical_data(stock['Code'], self.config.LOOKBACK_DAYS)
                
                # 2. 분석하기
                result = self.analyzer.analyze_breakout(stock, df)
                
                # 3. 보관
                if result:
                    breakout_stocks.append(result)
            except Exception:
                # 일부 상장폐지/정지 종목의 에러 무시
                continue

        # 4. 정렬
        breakout_stocks.sort(key=lambda x: x['deviation'], reverse=True)
        
        # 5. 리포트 생성 및 알림 발생
        msg = self._generate_report_message(breakout_stocks)
        print(msg)
        self.notifier.send_message(msg)

        # 6. 자동 매수 연동 (KIS API)
        if KisConfig.APP_KEY and KisConfig.APP_SECRET:
            print("\n🚨 KIS API 매매 연결 확인 완료. 모의/실전매매를 시도합니다.")
            for stock in breakout_stocks:
                print(f">>> {stock['name']}({stock['code']}) 시장가 매수 주문 전송 중...")
                self.kis_trader.order_market_buy(stock['code'], 1)  # 시장가 1주 매수
        else:
            print("\n🚫 Config 파일에 앱 키(APP_KEY/SECRET)가 입력되지 않아 API 자동매수가 스킵되었습니다.")

if __name__ == '__main__':
    bot = VWAPBot(Config)
    bot.run()
