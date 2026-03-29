import FinanceDataReader as fdr
from datetime import datetime, timedelta
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class MarketDataProvider:
    """외부 API(FinanceDataReader)로부터 시세/종목 정보를 수집해오는 데이터 소스 클래스"""
    @staticmethod
    def get_kospi_top_n(n):
        df_marcap = fdr.StockListing('KRX-MARCAP')
        
        try:
            admin_codes = set(fdr.StockListing('KRX-ADMIN')['Symbol'])
        except Exception:
            admin_codes = set()
            
        try:
            etf_codes = set(fdr.StockListing('ETF/KR')['Symbol'])
        except Exception:
            etf_codes = set()

        kospi_df = df_marcap[df_marcap['Market'] == 'KOSPI'].copy()
        kospi_df = kospi_df.sort_values(by='Marcap', ascending=False)
        
        top_stocks = []
        for _, row in kospi_df.iterrows():
            code = row['Code']
            name = row['Name']
            
            # 관리종목, ETF, 우선주 필터링 로직
            if code in admin_codes or code in etf_codes or not code.endswith('0'):
                continue
            if any(name.endswith(suffix) for suffix in ['우', '우B', '우(전환)', '우C']):
                continue
                
            top_stocks.append({'Code': code, 'Name': name})
            if len(top_stocks) >= n:
                break
                
        return top_stocks

    @staticmethod
    def get_historical_data(code, days_back):
        start_date = (datetime.today() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        return fdr.DataReader(code, start_date)
