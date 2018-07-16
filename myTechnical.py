# 自作パラボリックSAR
def psar(self, df_candleStick, acceleration = 0.02, maximum = 0.2):
    length = len(df_candleStick.index)
    high = df_candleStick['high']
    low = df_candleStick['low']
    close = df_candleStick['close']
    psar = [0 for i in range(len(df_candleStick.index))]
    trend = [True for i in range(len(df_candleStick.index))]
    af = acceleration
    ep = [0 for i in range(len(df_candleStick.index))]

    for i in range(1,length):

        # 最初は終値でトレンド判定
        if i == 1:
            if close[1] > close[0]:
                trend[1] = True
                ep[1] = high[1]
                psar[1] = high[0]
            else:
                trend[1] = False
                ep[1] = low[1]
                psar[1] = low[0]
            continue
        
        # トレンドを更新
        if trend[i-1]:
            if low[i] < psar[i-1]:
                trend[i] = False
            else:
                trend[i] = trend[i-1]
        else:
            if high[i] > psar[i-1]:
                trend[i] = True
            else:
                trend[i] = trend[i-1]

        # ep（最大・最小）を更新する
        if trend[i]:
            if low[i] < psar[i-1]:
                ep[i] = low[i]
            else:
                ep[i] = max(high[i], ep[i-1])
        else:
            if high[i] > psar[i-1]:
                ep[i] = high[i]
            else:
                ep[i] = min(low[i], ep[i-1])
        
        # パラボリックSAR値を計算する
        if trend[i] == trend[i-1]:
            if ep[i] != ep[i-1]:
                af = min(af + acceleration, maximum)
            psar[i] = psar[i - 1] + af * (ep[i] - psar[i - 1])
        else:
            af = acceleration
            psar[i] = ep[i-1]

    return psar
