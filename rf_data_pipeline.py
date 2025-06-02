import urllib.parse
import boto3
import pandas as pd
import io
import logging

logger = logging.getLogger('rf_logger')
handler = logging.StreamHandler()
logger.addHandler(hdlr=handler)
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')

def read_s3_csv(bucket_name: str, key: str):
    rf_bucket = s3.Bucket(name=bucket_name)
    fo = io.BytesIO()
    rf_bucket.download_fileobj(Key=key, Fileobj=fo)
    fo.seek(0)
    return fo

def get_cpu_spikes(df: pd.DataFrame) -> pd.DataFrame:
    cpu_std = df['CPU Usage'].std()
    cpu_mean = df['CPU Usage'].mean()
    df['cpu_deviation'] = df['CPU Usage'] - cpu_mean
    df['cpu_spike'] = df['cpu_deviation'].apply(lambda x: x > 2 * cpu_std)
    df_cpu_spike = df[df['cpu_spike'] == True]
    return df_cpu_spike
    

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    fo = read_s3_csv(bucket_name, key)
    df = pd.read_csv(fo)

    df_cpu_spike = get_cpu_spikes(df)
    df_cpu_spike.to_csv(path_or_buf=f's3://{bucket_name}/cpu_spikes/{key}')
