# QuantConnect Dataset Issue #19557: Missing Crypto Futures Minute Data (BTCUSDT, ETHUSDT)

## Overview

This issue concerns missing minute-resolution historical data for **BTCUSDT** and **ETHUSDT** crypto futures on the **Binance** market, as accessed via QuantConnect. The data gap occurs **between February 4, 2025, 12:00 AM and April 24, 2025, 12:00 AM**, specifically when queried with **fill-forward disabled**.

The missing data affects close prices (and potentially other OHLCV fields), leading to visible gaps in charts and inaccurate analysis results.

---

## Reproduction with QuantBook

The following code demonstrates the issue using QuantConnect’s QuantBook environment:

```python
from AlgorithmImports import *

qb = QuantBook()
symbol = qb.add_crypto_future("BTCUSDT", market=Market.BINANCE, fill_forward=False).symbol
history = qb.history(symbol, datetime(2025,2,1), datetime(2025,5,1), Resolution.MINUTE)
history.droplevel('symbol').close.plot()

## Root Cause Analysis

QuantConnect sources crypto futures data from **CoinAPI**, which aggregates data from Binance’s public APIs and public data feeds. Upon investigation, the missing data appears to be caused by **upstream issues on Binance's end** rather than a bug within QuantConnect.

### Contributing Events

1. **Binance Platform Outage — February 2025**  
   A significant outage impacted account access and trading operations. This likely delayed historical data processing.  
   📎 [Source](https://www.binance.com/en/square/post/21656107361106)

2. **Crypto Market Crash — March 9, 2025**  
   Amid U.S. trade tariffs, the crypto market saw a sharp decline (20.2% in February), causing extreme volatility. This may have overwhelmed Binance’s data logging infrastructure.  
   📎 [Source](https://www.binance.com/en/square/post/21326784028217)

3. **AWS Outage in Tokyo — April 15, 2025**  
   A widespread AWS outage affected Binance services, disrupting network access and temporarily halting withdrawals. This likely interfered with Binance's data feeds and historical data continuity.  
   📎 [Crypto.News](https://crypto.news/binance-multi-layered-challenges-april-2025/)  
   📎 [Reuters](https://www.reuters.com/technology/binance-services-start-recover-after-network-interruption-2025-04-15/)  
   📎 [CoinDesk](https://www.coindesk.com/markets/2025/04/15/binance-kucoin-and-other-crypto-firms-hit-by-amazon-web-service-issue)

4. **Binance GitHub Data Delay — Post-February 2025**  
   Binance’s public data repository shows that monthly kline updates (including spot and futures) were delayed or missing after February 2025.  
   📎 [GitHub Issue #438](https://github.com/binance/binance-public-data/issues)

The above events align with the observed missing data period (**Feb 4 to Apr 24, 2025**), indicating that the issue originates from **Binance's data availability** and was propagated via CoinAPI to QuantConnect.

---

## Verification: Estimating Missing Minutes

To validate the data gap, we compare the expected number of minute-resolution data points to the actual returned count.

### Expected Minute Bars

- **Date Range:** Feb 1 – May 1, 2025 = 89 days  
- **Minutes per Day:** 1440  
- **Total Expected Minutes:** Expected = 89 * 1440 = 128,160 


### Missing Period (Feb 4 – Apr 24, 2025)

- **Total Missing Days:**  
- February: 24 days (Feb 4–29)  
- March: 31 days  
- April: 24 days (Apr 1–24)  
- **Total:** 79 days  
- **Total Missing Minutes:**  so missing minutes = 79*1440 = 113,760.


