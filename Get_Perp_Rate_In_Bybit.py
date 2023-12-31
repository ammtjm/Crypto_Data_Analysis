# Purpose: Get Perpetual Funding Rate In Bybit
import requests
import pandas as pd
from pybit._v5_market import MarketHTTP

# Get Perpetual Funding Rate In Bybit
# Return: DataFrame
#TODO:  1.symbolを引数に取るようにする
#TODO: 2.取得するデータの期間を引数に取るようにする

# Get All Futures Symbols
# Return: List
def get_all_futures_symbols():
    url = "https://api.bybit.com/v2/public/symbols"
    response = requests.get(url)
    data = response.json()

    if data["ret_code"] != 0:
        print(f"Error: {data['ret_msg']}")
        return []

    symbols = [item["name"] for item in data["result"]]
    return symbols

# Get Funding Rates
def get_funding_rates(symbols,n_limit):
    market_http = MarketHTTP()
    data = market_http.get_funding_rate_history(category="linear",symbol=symbols, limit=n_limit)
    
    # 返り値の中身が空の場合はエラーをプリントして、空のDataFrameを返す
    if data["retCode"] != 0:
        print(f"Error: {data['retMsg']}")
        return pd.DataFrame()
    # fundingRateが0より大きいものだけ抽出,dataはdict型であるため、data["result"]でリストを取得
    # print(data)
    # 中身の確認
    funding_rates = data["result"]["list"]
    #positive_rates = [item for item in funding_rates if float(item["fundingRate"]) > 0]
    #sorted_rates = sorted(positive_rates, key=lambda x: float(x["fundingRate"]), reverse=True)

    df = pd.DataFrame(funding_rates)
    df['fundingRateTimestamp'] = pd.to_datetime(df['fundingRateTimestamp'].astype(int), unit='ms')

    return df


if __name__ == "__main__":
    symbol_list = get_all_futures_symbols()
    print(symbol_list)

    df_all = pd.DataFrame()
    for symbol in symbol_list:
        df = get_funding_rates(symbol, 1)
        df_all = pd.concat([df_all, df], axis=0)
    df_all = df_all.sort_values(by='fundingRate', ascending=False)
    print(df_all)
    #df = get_funding_rates()
    #print(df)


