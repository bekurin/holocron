import ssl
import pandas as pd
from datetime import datetime, timedelta
import FinanceDataReader as fdr

ssl._create_default_https_context = ssl._create_unverified_context

def main():
    print("Fetching listings...")
    df_marcap = fdr.StockListing('KRX-MARCAP')
    
    try:
        df_admin = fdr.StockListing('KRX-ADMIN')
        admin_codes = set(df_admin['Symbol'])
    except:
        admin_codes = set()
    
    try:
        df_etf = fdr.StockListing('ETF/KR')
        etf_codes = set(df_etf['Symbol'])
    except:
        etf_codes = set()

    kospi_df = df_marcap[df_marcap['Market'] == 'KOSPI'].copy()
    kospi_df = kospi_df.sort_values(by='Marcap', ascending=False)
    
    top_200 = []
    
    for _, row in kospi_df.iterrows():
        code = row['Code']
        name = row['Name']
        
        if code in admin_codes or code in etf_codes:
            continue
            
        # Preferred stocks exclusion
        if not code.endswith('0'):
            continue
            
        if any(name.endswith(suffix) for suffix in ['우', '우B', '우(전환)', '우C']):
            continue
            
        top_200.append({'Code': code, 'Name': name})
        
        if len(top_200) >= 200:
            break
            
    print(f"Collected top {len(top_200)} KOSPI stocks.")
    
    start_date = (datetime.today() - timedelta(days=365*2)).strftime('%Y-%m-%d')
    print(f"Fetching OHLCV data from {start_date} to today...")

    all_data = []
    
    for i, stock in enumerate(top_200):
        code = stock['Code']
        name = stock['Name']
        if i % 10 == 0:
            print(f"Fetching data for {i+1}/200: {name} ({code})")
        
        try:
            df = fdr.DataReader(code, start_date)
            if not df.empty:
                df['종목코드'] = code
                df['종목명'] = name
                df = df.reset_index()
                all_data.append(df)
        except Exception as e:
            print(f"Error fetching {name} ({code}): {e}")
            
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.rename(columns={
            'Date': '일자',
            'Open': '시가',
            'High': '고가',
            'Low': '저가',
            'Close': '종가',
            'Volume': '거래량'
        })
        
        columns_ordered = ['일자', '종목명', '종목코드', '시가', '고가', '종가', '저가', '거래량']
        columns_ordered = [col for col in columns_ordered if col in final_df.columns]
        
        final_df = final_df[columns_ordered]
        
        filename = 'kospi_top200_2years.csv'
        final_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Successfully saved {filename}")
    else:
        print("No data collected.")

if __name__ == '__main__':
    main()
