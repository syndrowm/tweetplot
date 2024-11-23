#!/usr/bin/env python
import pandas as pd
import json
from datetime import datetime
import pytz

JS_HEADER = b'window.YTD.tweet_headers.part0 = '

def load_data(bytes_data):
    if not bytes_data.startswith(JS_HEADER):
        raise ValueError("Invalid header")

    bytes_data =  bytes_data.lstrip(JS_HEADER)
    return json.loads(bytes_data)

def extract_created_times(data, tz='US/Mountain'):
    output_tz = pytz.timezone(tz)
    times = []
    for i in data:
        t = i['tweet']['created_at']
        dt = datetime.strptime(t, '%a %b %d %H:%M:%S %z %Y')
        local = dt.astimezone(output_tz)
        date=local.strftime('%Y-%m-%d')
        time=local.strftime('%H:%M')
        times.append((date, time))

    df = pd.DataFrame(times, columns=["date", "time"])
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df['time_only'] = pd.to_datetime(df['time'], format='%H:%M')
    return df


if __name__ == "__main__":

    data = load_data(open('tweet-headers.js', 'rb').read())
    df = extract_created_times(data)
