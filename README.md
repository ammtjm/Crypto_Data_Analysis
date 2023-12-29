# Bybitデルタニュートラル戦略
## ファイル構成
### Get_Perp_Rate_In_Bybit.py: Bybitのperpレート取得


### 概要
### 実行順序

```mermaid
graph LR
    A[sp500銘柄コード取得.py] --> B[sp500株価取得.py]
    B --> C[セクター別時価総額算出.py]
```