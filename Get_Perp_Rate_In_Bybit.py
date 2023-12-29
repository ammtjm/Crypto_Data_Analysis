# Purpose: Get Perpetual Funding Rate In Bybit
import requests
import pandas as pd
from pybit._v5_market import MarketHTTP

# Get Perpetual Funding Rate In Bybit
# Return: DataFrame
def get_funding_rates():
    market_http = MarketHTTP()
    data = market_http.get_funding_rate_history(category="linear",symbol="BTCUSDT", limit=1000)
    
    # 返り値の中身が空の場合はエラーをプリントして、空のDataFrameを返す
    if data["retCode"] != 0:
        print(f"Error: {data['retMsg']}")
        return pd.DataFrame()
    # fundingRateが0より大きいものだけ抽出,dataはdict型であるため、data["result"]でリストを取得
    # print(data)
    # 中身の確認
    funding_rates = data["result"]["list"]
    positive_rates = [item for item in funding_rates if float(item["fundingRate"]) > 0]
    sorted_rates = sorted(positive_rates, key=lambda x: float(x["fundingRate"]), reverse=True)

    df = pd.DataFrame(sorted_rates)
    df['fundingRateTimestamp'] = pd.to_datetime(df['fundingRateTimestamp'].astype(int), unit='ms')

    return df

if __name__ == "__main__":
    df = get_funding_rates()
    print(df)