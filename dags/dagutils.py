import pandas as pd
import re

def store_data_cleaner():
    df = pd.read_csv('/usr/local/airflow/store_files_airflow/raw_store_transactions.csv')

    def clean_store_location(st_loc):
        return re.sub(r'[^\w\s]', '', st_loc).strip()
    
    def clean_product_id(pd_id):
        matches = re.findall(r'\d+', pd_id)
        if matches:
            return matches[0]
        return pd_id
    
    def remove_dollar(amount):
        return float(amount.replace('$', ''))
    
    df['STORE_LOCATION'] = df['STORE_LOCATION'].apply(clean_store_location)
    df['PRODUCT_ID'] = df['PRODUCT_ID'].apply(clean_product_id)
    for to_clean in ['MRP', 'CP', 'DISCOUNT', 'SP']:
        df[to_clean] = df[to_clean].apply(remove_dollar)
    
    df.to_csv('/usr/local/airflow/store_files_airflow/clean_store_transactions.csv', index=False)
    print('Data cleaning complete!')
