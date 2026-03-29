document.addEventListener('DOMContentLoaded', () => {
    const CSV_URL = 'kospi_top200_2years.csv';
    const state = {
        data: [],      // Processed stock signals
        period: parseInt(document.getElementById('vwap-period').value), // e.g. 20
        filter: document.getElementById('filter-signal').value // e.g. 'all'
    };
    
    // UI Elements
    const elements = {
        loading: document.getElementById('loading'),
        tableSection: document.querySelector('.table-section'),
        tbody: document.getElementById('table-body'),
        statBreakout: document.getElementById('stat-breakout'),
        statUptrend: document.getElementById('stat-uptrend'),
        statDowntrend: document.getElementById('stat-downtrend'),
        statBreakdown: document.getElementById('stat-breakdown'),
        resultCount: document.getElementById('result-count'),
        lastDate: document.getElementById('last-date'),
        periodSelect: document.getElementById('vwap-period'),
        filterSelect: document.getElementById('filter-signal'),
        vwapHeaderLabel: document.getElementById('vwap-label-header')
    };

    // Initialization
    function init() {
        Papa.parse(CSV_URL, {
            download: true,
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                processRawData(results.data);
            },
            error: function(err) {
                console.error("CSV loading error:", err);
                elements.loading.innerHTML = '<h2>데이터 로드 실패</h2><p>CSV 파일 불러오는 중 오류가 발생했습니다.</p>';
            }
        });

        // Event Listeners for UI interaction
        elements.periodSelect.addEventListener('change', (e) => {
            state.period = parseInt(e.target.value);
            elements.vwapHeaderLabel.textContent = `${state.period}일`;
            // Re-process with new period
            Papa.parse(CSV_URL, {
                download: true,
                header: true,
                skipEmptyLines: true,
                complete: function(results) {
                    processRawData(results.data);
                }
            });
        });

        elements.filterSelect.addEventListener('change', (e) => {
            state.filter = e.target.value;
            renderView();
        });
    }

    // Processing raw CSV rows
    function processRawData(rows) {
        // Group by ticker
        const grouped = {};
        let maxDate = '';

        rows.forEach(row => {
            if(!row['종목코드'] || !row['일자']) return;
            const code = row['종목코드'];
            if(!grouped[code]) {
                grouped[code] = {
                    code: code,
                    name: row['종목명'],
                    history: []
                };
            }
            
            if (row['일자'] > maxDate) maxDate = row['일자'];

            grouped[code].history.push({
                date: row['일자'],
                open: parseFloat(row['시가']),
                high: parseFloat(row['고가']),
                low: parseFloat(row['저가']),
                close: parseFloat(row['종가']),
                volume: parseFloat(row['거래량']),
            });
        });

        elements.lastDate.textContent = maxDate;

        const pData = [];
        const N = state.period;

        Object.keys(grouped).forEach(code => {
            const stock = grouped[code];
            // Sort by date ascending (oldest to newest)
            stock.history.sort((a,b) => a.date.localeCompare(b.date));
            
            if(stock.history.length < Math.max(N + 1, 5)) return; // not enough data

            // Slice out the exact number of days we need to calculate
            // For Today's VWAP, we need last N days. For yesterday's, we need from -N-1 to -2.
            const history = stock.history;
            const len = history.length;
            
            // Get last 2 days info
            const today = history[len-1];
            const yesterday = history[len-2];

            // Helper: compute N-day VWAP ending at endIdx inclusive
            const computeVWAP = (endIdx) => {
                let sumPv = 0;
                let sumVol = 0;
                const startIdx = Math.max(0, endIdx - N + 1);
                for(let i=startIdx; i<=endIdx; i++) {
                    const row = history[i];
                    const TP = (row.high + row.low + row.close) / 3;
                    sumPv += TP * row.volume;
                    sumVol += row.volume;
                }
                return sumVol === 0 ? today.close : (sumPv / sumVol);
            };

            const todayVWAP = computeVWAP(len - 1);
            const yesterdayVWAP = computeVWAP(len - 2);

            // Signal Logic
            let signal = '';
            if(yesterday.close <= yesterdayVWAP && today.close > todayVWAP) {
                signal = 'breakout';
            } else if(yesterday.close >= yesterdayVWAP && today.close < todayVWAP) {
                signal = 'breakdown';
            } else if(today.close > todayVWAP) {
                signal = 'uptrend';
            } else {
                signal = 'downtrend';
            }

            // Deviation
            const deviation = ((today.close - todayVWAP) / todayVWAP) * 100;

            // Volume surge comparison (today vs prev 5 day avg)
            let volAvg5 = 0;
            for(let i = len-6; i < len-1; i++) volAvg5 += history[i].volume;
            volAvg5 /= 5;
            const volRatio = today.volume / volAvg5;

            pData.push({
                code: stock.code,
                name: stock.name,
                close: today.close,
                vwap: todayVWAP,
                deviation: deviation,
                volRatio: volRatio,
                signal: signal
            });
        });

        // Store and sort globally (Breakouts > Uptrend > Breakdown > Downtrend, sub-sort by deviation)
        const signaWeight = { 'breakout': 1, 'uptrend': 2, 'breakdown': 3, 'downtrend': 4 };
        pData.sort((a, b) => {
            if(signaWeight[a.signal] !== signaWeight[b.signal]) return signaWeight[a.signal] - signaWeight[b.signal];
            return b.deviation - a.deviation;
        });

        state.data = pData;

        // Hide loading, show table
        elements.loading.style.display = 'none';
        elements.tableSection.style.display = 'block';

        renderView();
    }

    function renderView() {
        const pData = state.data;
        const filter = state.filter;

        // Reset Stats
        let totals = { breakout: 0, uptrend: 0, breakdown: 0, downtrend: 0 };
        pData.forEach(s => totals[s.signal]++);

        elements.statBreakout.textContent = totals.breakout;
        elements.statUptrend.textContent = totals.uptrend;
        elements.statBreakdown.textContent = totals.breakdown;
        elements.statDowntrend.textContent = totals.downtrend;

        // Filter and Render Rows
        let htmlMarkup = '';
        let count = 0;

        pData.forEach(item => {
            if(filter !== 'all' && item.signal !== filter) return;

            const devStr = item.deviation > 0 ? `+${item.deviation.toFixed(2)}%` : `${item.deviation.toFixed(2)}%`;
            const devClass = item.deviation > 0 ? 'pc-positive' : (item.deviation < 0 ? 'pc-negative' : 'pc-neutral');
            
            const volStr = `${(item.volRatio * 100).toFixed(0)}%`;
            const volClass = item.volRatio > 2 ? 'vol-surge' : '';

            let badgeHtml = '';
            switch(item.signal) {
                case 'breakout': badgeHtml = `<div class="badge breakout">🚀 상승 돌파</div>`; break;
                case 'uptrend': badgeHtml = `<div class="badge uptrend">📈 상승 추세</div>`; break;
                case 'breakdown': badgeHtml = `<div class="badge breakdown">📉 하락 돌파</div>`; break;
                case 'downtrend': badgeHtml = `<div class="badge downtrend">⚠️ 하락 유지</div>`; break;
            }

            htmlMarkup += `
                <tr>
                    <td class="col-code">${item.code}</td>
                    <td class="col-name">${item.name}</td>
                    <td class="col-price">₩${item.close.toLocaleString()}</td>
                    <td>₩${Math.round(item.vwap).toLocaleString()}</td>
                    <td class="${devClass}">${devStr}</td>
                    <td class="${volClass}">${volStr}</td>
                    <td>${badgeHtml}</td>
                </tr>
            `;
            count++;
        });

        elements.tbody.innerHTML = htmlMarkup;
        elements.resultCount.textContent = count;
    }

    init();
});
