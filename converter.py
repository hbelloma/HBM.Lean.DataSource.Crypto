import pandas as pd
import zipfile
import os

def convert_to_lean(input_file, output_dir):
    df = pd.read_csv(input_file)
    symbol = "BTCUSD"  # Map to LEAN symbol
    os.makedirs(output_dir, exist_ok=True)
    
    for date, row in df.groupby('timestamp'):
        zip_path = f"{output_dir}/{date.replace('-', '')}_{symbol.lower()}.zip"
        with zipfile.ZipFile(zip_path, 'w') as z:
            csv_content = f"{row['open'].values[0]},{row['high'].values[0]},{row['low'].values[0]},{row['close'].values[0]},{row['volume'].values[0]}\n"
            z.writestr(f"{symbol.lower()}.csv", csv_content)

convert_to_lean("data/raw/bitcoin.csv", "data/processed")