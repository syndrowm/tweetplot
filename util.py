#!/usr/bin/env python
import io
from datetime import datetime

import pandas as pd
import pytz

JS_HEADER = b"window.YTD.tweet_headers.part0 = "


def load_data(bytes_data, tz="US/Mountain"):
    if not bytes_data.startswith(JS_HEADER):
        raise ValueError("Invalid header")

    bytes_data = bytes_data.lstrip(JS_HEADER)
    df = pd.read_json(io.BytesIO(bytes_data))
    df["created_at"] = df["tweet"].apply(lambda x: pd.to_datetime(x["created_at"]))
    df["localtime"] = df["created_at"].dt.tz_convert(tz)
    return df


if __name__ == "__main__":

    df = load_data(open("tweet-headers.js", "rb").read())
