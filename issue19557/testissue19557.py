from AlgorithmImports import *
from datetime import datetime, timedelta

qb = QuantBook()
symbol = qb.AddCryptoFuture("BTCUSDT", market=Market.BINANCE, fillForward=False).Symbol
history = qb.History(symbol, datetime(2025, 2, 1), datetime(2025, 5, 1), Resolution.Minute).droplevel('symbol')

# Calculate expected minutes: (end - start) in minutes
start = datetime(2025, 2, 1)
end = datetime(2025, 5, 1)
expected_minutes = int((end - start).total_seconds() / 60)

#print(f"Expected minutes: {expected_minutes}")

# Actual data points
actual_points = len(history)

# Identify the gaps in the data: Check for timestamps not incrementing by 1 minute
gaps = []
prev_time = None
for index, row in history.iterrows():
    current_time = index
    if prev_time and (current_time - prev_time) > timedelta(minutes=1):
        gaps.append(f"Gap from {prev_time} to {current_time}")
    prev_time = current_time

print(f"Expected data points: {expected_minutes}") 
# Expected data points: 128160
print(f"Actual data points: {actual_points}")
print(f"Missing points: {expected_minutes - actual_points}")
if gaps:
    print("Detected gaps:")
    for gap in gaps:
        print(gap)
else:
    print("No gaps detected.")

# To plot for visual proof (as in original query):
history.close.plot()

