<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日股票資訊儀表板</title>
    
    <!-- 引入 Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- 引入 Chart.js 用於繪製股票走勢圖 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- 引入 FontAwesome 圖示 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- 設定 Tailwind 自訂主題與字體 -->
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'Noto Sans TC', 'sans-serif'],
                    },
                    colors: {
                        gray: {
                            850: '#1f2937',
                            900: '#111827',
                            950: '#030712',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+TC:wght@300;400;500;700&display=swap');
        body {
            background-color: #030712; /* gray-950 */
            color: #f3f4f6; /* gray-100 */
        }
        /* 隱藏滾動條但保留功能 */
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .shimmer {
            animation: shimmer 2s infinite linear;
            background: linear-gradient(to right, #1f2937 4%, #374151 25%, #1f2937 36%);
            background-size: 1000px 100%;
        }
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col font-sans antialiased selection:bg-blue-500 selection:text-white">

    <!-- 頂部導覽列 -->
    <header class="sticky top-0 z-50 bg-gray-900/80 backdrop-blur-md border-b border-gray-800 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
                <div class="flex-shrink-0 flex items-center gap-3 cursor-pointer">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                        <i class="fa-solid fa-chart-line text-white text-xl"></i>
                    </div>
                    <span class="font-bold text-xl tracking-wide hidden sm:block">Stock<span class="text-blue-400">View</span> 股市雷達</span>
                </div>

                <!-- 搜尋列 -->
                <div class="flex-1 max-w-xl mx-4">
                    <form id="search-form" class="relative group">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-solid fa-magnifying-glass text-gray-400 group-focus-within:text-blue-400 transition-colors"></i>
                        </div>
                        <input type="text" id="search-input" 
                            class="block w-full pl-10 pr-3 py-2.5 border border-gray-700 rounded-xl leading-5 bg-gray-800 text-gray-200 placeholder-gray-400 focus:outline-none focus:bg-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 sm:text-sm transition-all shadow-inner" 
                            placeholder="輸入股票代號，例如: AAPL, TSLA, 2330.TW..." 
                            autocomplete="off" required>
                        <button type="submit" class="absolute inset-y-1 right-1 px-4 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-lg transition-colors shadow-sm">
                            搜尋
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </header>

    <!-- 主要內容區 -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- 歡迎/初始畫面 -->
        <div id="initial-state" class="flex flex-col items-center justify-center py-20 text-center space-y-6">
            <div class="w-24 h-24 bg-gray-800 rounded-full flex items-center justify-center shadow-inner">
                <i class="fa-solid fa-magnifying-glass-chart text-4xl text-gray-500"></i>
            </div>
            <div class="space-y-2">
                <h2 class="text-2xl font-bold text-gray-200">開始探索全球市場</h2>
                <p class="text-gray-400 max-w-md mx-auto">請在上方搜尋列輸入您感興趣的股票代號（例如 AAPL 或 2330.TW），即可獲取最新的每日行情與市場資訊。</p>
            </div>
            <div class="flex gap-3 pt-4">
                <button onclick="document.getElementById('search-input').value='AAPL'; document.getElementById('search-form').dispatchEvent(new Event('submit'))" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm font-medium text-gray-300 transition-colors border border-gray-700">熱門: AAPL</button>
                <button onclick="document.getElementById('search-input').value='TSLA'; document.getElementById('search-form').dispatchEvent(new Event('submit'))" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm font-medium text-gray-300 transition-colors border border-gray-700">熱門: TSLA</button>
                <button onclick="document.getElementById('search-input').value='2330.TW'; document.getElementById('search-form').dispatchEvent(new Event('submit'))" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm font-medium text-gray-300 transition-colors border border-gray-700">熱門: 2330.TW</button>
            </div>
        </div>

        <!-- 載入中動畫 (骨架屏) -->
        <div id="loading-state" class="hidden flex-col gap-6">
            <div class="flex justify-between items-end">
                <div class="space-y-3 w-1/3">
                    <div class="h-8 w-24 shimmer rounded-md"></div>
                    <div class="h-12 w-48 shimmer rounded-md"></div>
                </div>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 h-96 shimmer rounded-2xl border border-gray-800"></div>
                <div class="grid grid-cols-2 gap-4 h-96">
                    <div class="shimmer rounded-2xl border border-gray-800"></div>
                    <div class="shimmer rounded-2xl border border-gray-800"></div>
                    <div class="shimmer rounded-2xl border border-gray-800"></div>
                    <div class="shimmer rounded-2xl border border-gray-800"></div>
                </div>
            </div>
        </div>

        <!-- 錯誤提示 -->
        <div id="error-message" class="hidden bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-xl flex items-start gap-3 mb-6">
            <i class="fa-solid fa-triangle-exclamation mt-1"></i>
            <div>
                <h3 class="font-bold">查詢失敗</h3>
                <p id="error-text" class="text-sm opacity-90 mt-1">找不到該股票代號的資訊，請確認代號是否正確。</p>
            </div>
        </div>

        <!-- 儀表板資料區塊 (隱藏直到有資料) -->
        <div id="dashboard-content" class="hidden flex-col gap-6 fade-in">
            
            <!-- 頂部：股票標題與目前價格 -->
            <div class="bg-gray-900 border border-gray-800 rounded-3xl p-6 md:p-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-6 shadow-xl relative overflow-hidden">
                <!-- 裝飾用背景光暈 -->
                <div class="absolute -top-24 -right-24 w-48 h-48 bg-blue-500/10 blur-3xl rounded-full pointer-events-none"></div>
                
                <div>
                    <div class="flex items-center gap-3 mb-2">
                        <h1 id="stock-symbol" class="text-3xl md:text-5xl font-black text-white tracking-tight">AAPL</h1>
                        <span id="stock-currency" class="px-2.5 py-1 bg-gray-800 text-gray-400 text-xs font-bold rounded-md border border-gray-700">USD</span>
                    </div>
                    <h2 id="stock-name" class="text-lg md:text-xl text-gray-400 font-medium">Apple Inc.</h2>
                </div>
                
                <div class="flex flex-col items-start md:items-end">
                    <div class="text-sm text-gray-400 mb-1 font-medium">目前股價 (即時)</div>
                    <div class="flex items-baseline gap-4">
                        <div id="stock-price" class="text-4xl md:text-6xl font-black tabular-nums tracking-tighter">150.00</div>
                        <div id="stock-change-container" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-bold text-lg md:text-xl">
                            <i id="stock-change-icon" class="fa-solid fa-caret-up"></i>
                            <span id="stock-change-value" class="tabular-nums">2.50</span>
                            <span id="stock-change-percent" class="tabular-nums">(1.69%)</span>
                        </div>
                    </div>
                    <div class="text-xs text-gray-500 mt-2 flex items-center gap-1.5">
                        <i class="fa-regular fa-clock"></i> 最後更新: <span id="last-update-time"></span>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- 左側：走勢圖表 -->
                <div class="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-3xl p-6 shadow-xl flex flex-col">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-lg font-bold text-gray-200 flex items-center gap-2">
                            <i class="fa-solid fa-chart-area text-blue-500"></i> 近30日走勢 (模擬)
                        </h3>
                        <!-- 假裝的圖表時間切換按鈕 -->
                        <div class="flex bg-gray-800 rounded-lg p-1 border border-gray-700">
                            <button class="px-3 py-1 text-xs font-medium bg-gray-700 text-white rounded-md shadow">1M</button>
                            <button class="px-3 py-1 text-xs font-medium text-gray-400 hover:text-white transition-colors disabled:opacity-50" disabled>3M</button>
                            <button class="px-3 py-1 text-xs font-medium text-gray-400 hover:text-white transition-colors disabled:opacity-50" disabled>1Y</button>
                        </div>
                    </div>
                    <div class="relative flex-1 w-full min-h-[300px]">
                        <canvas id="stockChart"></canvas>
                    </div>
                </div>

                <!-- 右側：詳細統計數據網格 -->
                <div class="grid grid-cols-2 gap-4">
                    <!-- 統計卡片組件 -->
                    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-5 flex flex-col justify-between hover:bg-gray-800/50 transition-colors">
                        <div class="text-gray-400 text-sm font-medium flex items-center gap-2 mb-2">
                            <i class="fa-solid fa-door-open opacity-50"></i> 開盤價
                        </div>
                        <div id="stat-open" class="text-2xl font-bold tabular-nums">--</div>
                    </div>
                    
                    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-5 flex flex-col justify-between hover:bg-gray-800/50 transition-colors">
                        <div class="text-gray-400 text-sm font-medium flex items-center gap-2 mb-2">
                            <i class="fa-solid fa-arrow-turn-down opacity-50"></i> 昨收價
                        </div>
                        <div id="stat-prev-close" class="text-2xl font-bold tabular-nums">--</div>
                    </div>

                    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-5 flex flex-col justify-between hover:bg-gray-800/50 transition-colors">
                        <div class="text-gray-400 text-sm font-medium flex items-center gap-2 mb-2">
                            <i class="fa-solid fa-arrow-trend-up text-emerald-500/70"></i> 最高價
                        </div>
                        <div id="stat-high" class="text-2xl font-bold tabular-nums text-emerald-400">--</div>
                    </div>

                    <div class="bg-gray-900 border border-gray-800 rounded-2xl p-5 flex flex-col justify-between hover:bg-gray-800/50 transition-colors">
                        <div class="text-gray-400 text-sm font-medium flex items-center gap-2 mb-2">
                            <i class="fa-solid fa-arrow-trend-down text-rose-500/70"></i> 最低價
                        </div>
                        <div id="stat-low" class="text-2xl font-bold tabular-nums text-rose-400">--</div>
                    </div>

                    <div class="col-span-2 bg-gray-900 border border-gray-800 rounded-2xl p-5 flex justify-between items-center hover:bg-gray-800/50 transition-colors relative overflow-hidden">
                        <div class="absolute right-0 bottom-0 opacity-5 transform translate-x-4 translate-y-4">
                            <i class="fa-solid fa-layer-group text-8xl"></i>
                        </div>
                        <div>
                            <div class="text-gray-400 text-sm font-medium flex items-center gap-2 mb-1">
                                <i class="fa-solid fa-chart-bar opacity-50"></i> 總成交量 (Volume)
                            </div>
                            <div id="stat-volume" class="text-3xl font-bold tabular-nums tracking-tight">--</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="text-center text-xs text-gray-600 mt-4">
                免責聲明：本儀表板顯示之數據皆為**前端動態生成的模擬數據**，僅供 UI/UX 展示與技術測試使用，不代表真實市場行情，亦不可作為任何投資決策之依據。
            </div>
        </div>
    </main>

    <script>
        // 設定 Chart.js 預設樣式以符合深色主題
        Chart.defaults.color = '#9ca3af';
        Chart.defaults.font.family = "'Inter', 'Noto Sans TC', sans-serif";
        Chart.defaults.scale.grid.color = 'rgba(75, 85, 99, 0.2)'; // gray-600 with opacity

        let stockChartInstance = null;

        /**
         * 格式化數字為貨幣格式 (例如: 1,234.56)
         */
        const formatCurrency = (num) => {
            return new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num);
        };

        /**
         * 格式化大數字 (例如: 1.2M, 3.4B)
         */
        const formatNumberToCompact = (num) => {
            return new Intl.NumberFormat('en-US', { notation: "compact", compactDisplay: "short" }).format(num);
        };

        /**
         * ==========================================
         * 🔌 關於串接真實 API 的說明 (教學註解)
         * ==========================================
         * 在真實的應用程式中，您不會在前端寫死資料，而是會透過 fetch() 呼叫第三方股票 API。
         * 常見的股票 API 提供商包含：Alpha Vantage, Finnhub, Polygon.io, Yahoo Finance API (透過 RapidAPI) 等。
         * 
         * ⚠️ 注意：大多數 API 都有 CORS (跨網域資源共用) 限制，且不建議將 API Key 直接暴露在前端 HTML/JS 中。
         * 標準做法是：建立一個自己的後端伺服器 (Node.js/Python 等)，前端向自己的後端請求，後端再帶著 API Key 去打真實的 API。
         * 
         * 以下是假設您有後端代理或允許前端呼叫的 API 時的寫法範例：
         * 
         * async function fetchRealStockData(symbol) {
         *     const apiKey = 'YOUR_API_KEY'; // 應藏於環境變數或後端
         *     // 範例：Finnhub Quote API
         *     const response = await fetch(`https://finnhub.io/api/v1/quote?symbol=${symbol}&token=${apiKey}`);
         *     if (!response.ok) throw new Error('API 請求失敗');
         *     const data = await response.json();
         *     
         *     // 將 API 回傳的資料映射到我們的 UI 欄位
         *     return {
         *         price: data.c,           // Current price
         *         change: data.d,          // Change
         *         changePercent: data.dp,  // Percent change
         *         open: data.o,            // Open price of the day
         *         high: data.h,            // High price of the day
         *         low: data.l,             // Low price of the day
         *         prevClose: data.pc,      // Previous close price
         *         // 成交量可能需要打另一個 API Endpoint 取得
         *     };
         * }
         */

        /**
         * 產生逼真的模擬股票數據 (基於股票代號產生特定的隨機數值)
         * 為了讓展示效果好，同一代號雖然是隨機生成，但數值之間符合基礎財務邏輯。
         */
        const generateMockStockData = (symbol) => {
            return new Promise((resolve, reject) => {
                // 模擬網路延遲 0.8 到 1.5 秒
                setTimeout(() => {
                    const upperSymbol = symbol.trim().toUpperCase();
                    
                    // 簡單的驗證：不能為空
                    if (!upperSymbol) {
                        reject(new Error("股票代號不能為空"));
                        return;
                    }

                    // 用字串長度和字元代碼產生一個基礎「價格範圍」
                    let baseSeed = 0;
                    for(let i = 0; i < upperSymbol.length; i++) {
                        baseSeed += upperSymbol.charCodeAt(i);
                    }
                    
                    // 產生基礎價格 (落在 10 到 800 之間)
                    const basePrice = (baseSeed % 790) + 10;
                    
                    // 產生每日變動 (-5% 到 +5%)
                    const dailyVolatility = (Math.random() * 0.1) - 0.05; 
                    const changeValue = basePrice * dailyVolatility;
                    
                    const currentPrice = basePrice + changeValue;
                    const prevClose = basePrice;
                    
                    // 計算最高/最低/開盤 (符合邏輯的範圍)
                    const openPrice = prevClose + (changeValue * (Math.random() * 0.5)); // 開盤價在昨收與現價之間
                    
                    const maxPrice = Math.max(currentPrice, openPrice);
                    const minPrice = Math.min(currentPrice, openPrice);
                    
                    const high = maxPrice + (maxPrice * Math.random() * 0.02); // 最高價略高於現價/開盤最大值
                    const low = minPrice - (minPrice * Math.random() * 0.02);  // 最低價略低於現價/開盤最小值

                    // 模擬成交量 (1百萬 到 1億)
                    const volume = Math.floor(Math.random() * 99000000) + 1000000;

                    // 假造公司名稱 (簡單判斷台灣股票與美股)
                    let compName = `${upperSymbol} Corporation`;
                    let currency = 'USD';
                    if (upperSymbol.includes('.TW') || !isNaN(upperSymbol)) {
                        compName = `${upperSymbol} 股份有限公司`;
                        currency = 'TWD';
                    } else if (upperSymbol === 'AAPL') compName = 'Apple Inc.';
                    else if (upperSymbol === 'TSLA') compName = 'Tesla, Inc.';
                    else if (upperSymbol === 'MSFT') compName = 'Microsoft Corporation';

                    // 產生過去 30 天的模擬歷史數據 (用於圖表)
                    const historyPrices = [];
                    const historyDates = [];
                    let histPrice = prevClose;
                    
                    // 倒推 30 天
                    const today = new Date();
                    for (let i = 30; i >= 1; i--) {
                        const date = new Date(today);
                        date.setDate(date.getDate() - i);
                        // 略過週末 (簡單處理，不考慮國定假日)
                        if(date.getDay() !== 0 && date.getDay() !== 6) {
                            historyDates.push(`${date.getMonth()+1}/${date.getDate()}`);
                            // 每日隨機變動 -2% 到 +2%
                            const change = histPrice * ((Math.random() * 0.04) - 0.02);
                            histPrice = histPrice + change;
                            historyPrices.push(histPrice);
                        }
                    }
                    // 加入今日資料
                    historyDates.push('Today');
                    historyPrices.push(currentPrice);

                    resolve({
                        symbol: upperSymbol,
                        name: compName,
                        currency: currency,
                        price: currentPrice,
                        change: changeValue,
                        changePercent: (changeValue / prevClose) * 100,
                        open: openPrice,
                        high: high,
                        low: low,
                        prevClose: prevClose,
                        volume: volume,
                        history: {
                            dates: historyDates,
                            prices: historyPrices
                        }
                    });

                }, 800 + Math.random() * 700);
            });
        };

        /**
         * 繪製或更新 Chart.js 圖表
         */
        const renderChart = (historyData, isPositive) => {
            const ctx = document.getElementById('stockChart').getContext('2d');
            
            // 決定走勢圖顏色：漲為綠(Emerald)，跌為紅(Rose)
            const lineColor = isPositive ? '#34d399' : '#fb7185';
            const gradientBg = ctx.createLinearGradient(0, 0, 0, 400);
            gradientBg.addColorStop(0, isPositive ? 'rgba(52, 211, 153, 0.2)' : 'rgba(251, 113, 133, 0.2)');
            gradientBg.addColorStop(1, 'rgba(17, 24, 39, 0)'); // 漸變至背景色

            if (stockChartInstance) {
                stockChartInstance.destroy();
            }

            stockChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: historyData.dates,
                    datasets: [{
                        label: '收盤價',
                        data: historyData.prices,
                        borderColor: lineColor,
                        backgroundColor: gradientBg,
                        borderWidth: 2,
                        pointRadius: 0, // 隱藏數據點，讓線條更平滑
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#1f2937',
                        pointBorderColor: lineColor,
                        pointBorderWidth: 2,
                        fill: true,
                        tension: 0.1 // 讓線條稍微平滑
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(17, 24, 39, 0.9)',
                            titleColor: '#9ca3af',
                            bodyColor: '#fff',
                            borderColor: 'rgba(75, 85, 99, 0.5)',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return `$${formatCurrency(context.parsed.y)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: {
                                maxTicksLimit: 6,
                                font: { size: 11 }
                            }
                        },
                        y: {
                            position: 'right',
                            grid: {
                                borderDash: [4, 4]
                            },
                            ticks: {
                                callback: function(value) { return value.toFixed(1); },
                                font: { size: 11 }
                            }
                        }
                    }
                }
            });
        };

        /**
         * 更新畫面上的所有資訊
         */
        const updateDashboardUI = (data) => {
            const isPositive = data.change >= 0;
            
            // 更新文字與基本數值
            document.getElementById('stock-symbol').textContent = data.symbol;
            document.getElementById('stock-name').textContent = data.name;
            document.getElementById('stock-currency').textContent = data.currency;
            document.getElementById('stock-price').textContent = formatCurrency(data.price);
            
            // 更新漲跌幅與顏色
            const changeContainer = document.getElementById('stock-change-container');
            const changeIcon = document.getElementById('stock-change-icon');
            const changeValue = document.getElementById('stock-change-value');
            const changePercent = document.getElementById('stock-change-percent');

            // 移除舊的顏色 class
            changeContainer.classList.remove('bg-emerald-500/10', 'text-emerald-400', 'bg-rose-500/10', 'text-rose-400', 'bg-gray-500/10', 'text-gray-400');
            changeIcon.className = 'fa-solid'; // reset icon

            if (data.change > 0) {
                changeContainer.classList.add('bg-emerald-500/10', 'text-emerald-400');
                changeIcon.classList.add('fa-caret-up');
                changeValue.textContent = '+' + formatCurrency(data.change);
                changePercent.textContent = `(+${data.changePercent.toFixed(2)}%)`;
            } else if (data.change < 0) {
                changeContainer.classList.add('bg-rose-500/10', 'text-rose-400');
                changeIcon.classList.add('fa-caret-down');
                // Math.abs 用於移除負號，由 UI 呈現
                changeValue.textContent = '-' + formatCurrency(Math.abs(data.change));
                changePercent.textContent = `(${data.changePercent.toFixed(2)}%)`;
            } else {
                changeContainer.classList.add('bg-gray-500/10', 'text-gray-400');
                changeIcon.classList.add('fa-minus');
                changeValue.textContent = '0.00';
                changePercent.textContent = '(0.00%)';
            }

            // 更新時間
            const now = new Date();
            document.getElementById('last-update-time').textContent = now.toLocaleTimeString('zh-TW', { hour12: false });

            // 更新統計網格
            document.getElementById('stat-open').textContent = formatCurrency(data.open);
            document.getElementById('stat-prev-close').textContent = formatCurrency(data.prevClose);
            document.getElementById('stat-high').textContent = formatCurrency(data.high);
            document.getElementById('stat-low').textContent = formatCurrency(data.low);
            document.getElementById('stat-volume').textContent = formatNumberToCompact(data.volume);

            // 繪製圖表
            renderChart(data.history, isPositive);
        };

        // 綁定表單送出事件
        document.getElementById('search-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const searchInput = document.getElementById('search-input').value.trim();
            if (!searchInput) return;

            // UI 狀態切換管理
            const initialState = document.getElementById('initial-state');
            const loadingState = document.getElementById('loading-state');
            const errorState = document.getElementById('error-message');
            const dashboardContent = document.getElementById('dashboard-content');
            
            // 隱藏其他狀態，顯示載入中
            initialState.classList.add('hidden');
            errorState.classList.add('hidden');
            dashboardContent.classList.add('hidden');
            dashboardContent.classList.remove('flex'); // 確保 flex 被移除以配合 hidden
            
            loadingState.classList.remove('hidden');
            loadingState.classList.add('flex');

            try {
                // 模擬 API 呼叫取得資料
                const stockData = await generateMockStockData(searchInput);
                
                // 更新 UI
                updateDashboardUI(stockData);
                
                // 隱藏載入中，顯示資料
                loadingState.classList.add('hidden');
                loadingState.classList.remove('flex');
                
                dashboardContent.classList.remove('hidden');
                dashboardContent.classList.add('flex');
                
                // 讓輸入框失去焦點以收起手機鍵盤
                document.getElementById('search-input').blur();

            } catch (error) {
                console.error("獲取資料失敗:", error);
                
                // 隱藏載入中，顯示錯誤
                loadingState.classList.add('hidden');
                loadingState.classList.remove('flex');
                
                errorState.classList.remove('hidden');
                // 如果是第一次搜尋失敗，維持顯示初始畫面
                if (document.getElementById('stock-symbol').textContent === 'AAPL' && dashboardContent.classList.contains('hidden')) {
                     initialState.classList.remove('hidden');
                }
            }
        });
    </script>
</body>
</html>
