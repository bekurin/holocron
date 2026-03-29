class VWAPAnalyzer:
    """순수하게 VWAP 데이터를 정제하고 신호를 판별하는 비즈니스 도메인 클래스"""
    def __init__(self, period):
        self.period = period

    def _calculate_vwap(self, history, end_idx):
        sum_pv = 0
        sum_vol = 0
        start_idx = max(0, end_idx - self.period + 1)
        for i in range(start_idx, end_idx + 1):
            row = history[i]
            tp = (row['High'] + row['Low'] + row['Close']) / 3
            sum_pv += tp * row['Volume']
            sum_vol += row['Volume']
            
        return history[end_idx]['Close'] if sum_vol == 0 else sum_pv / sum_vol

    def analyze_breakout(self, stock, df):
        """특정 종목의 VWAP 돌파 여부를 평가하여 조건 부합 시 dict 반환, 아니면 None"""
        if len(df) < self.period + 2:
            return None
            
        history = df.reset_index().to_dict('records')
        len_hist = len(history)
        today = history[len_hist-1]
        yesterday = history[len_hist-2]

        today_vwap = self._calculate_vwap(history, len_hist - 1)
        yesterday_vwap = self._calculate_vwap(history, len_hist - 2)

        # 상태 판단: 전날 VWAP 이하 -> 당일 VWAP 상향 돌파
        if yesterday['Close'] <= yesterday_vwap and today['Close'] > today_vwap:
            deviation = ((today['Close'] - today_vwap) / today_vwap) * 100
            
            vol_avg5 = sum([history[i]['Volume'] for i in range(len_hist-6, len_hist-1)]) / 5
            vol_ratio = (today['Volume'] / vol_avg5) * 100 if vol_avg5 > 0 else 0
            
            return {
                'name': stock['Name'],
                'code': stock['Code'],
                'price': today['Close'],
                'vwap': today_vwap,
                'deviation': deviation,
                'vol_ratio': vol_ratio
            }
        return None
