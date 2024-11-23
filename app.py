#!/usr/bin/env python
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pytz
import io
from util import (load_data, extract_created_times)

st.set_page_config(
    page_title="Tweet Scatter plot",
    page_icon="🦋",
)

def main():

    with st.sidebar:
   
        st.markdown("---")
        timezone = st.selectbox("Choose your timezone", pytz.all_timezones, index=pytz.all_timezones.index("US/Mountain"))
        st.markdown("---")
        uploaded_file = st.file_uploader("Choose your tweet-headers.js file")
        st.markdown("---")
        st.sidebar.markdown("Created by [Evan Anderson](https://bsky.app/profile/syndrowm.com)")


    st.title('Tweet addict scatter plot')


    if uploaded_file is not None and timezone is not None:
        try:
            df = load_data(uploaded_file.getvalue())
        except Exception as exc:
            st.error(f"Invalid file data. Please upload the tweets.js file. {exc}", icon="☠️")
            return

        chart_data = extract_created_times(df, tz=timezone)

        #chart_data = pd.DataFrame(times, columns=["year", "time"])
        #chart_data['datetime'] = pd.to_datetime(chart_data['year'] + ' ' + chart_data['time'])
        #chart_data['time_only'] = pd.to_datetime(chart_data['time'], format='%H:%M')

        c = (
            alt.Chart(chart_data)
            .mark_circle()
            .mark_point(size=5, opacity=0.7)
            .encode(
                x=alt.X('datetime:T', title='Year', axis=alt.Axis(format='%Y', tickCount='year', grid=True, gridDash=[4,4])),  # Ordinal for discrete years
                y=alt.Y(
                    'time_only:T', 
                    title=f'Time of Tweet ({timezone})',
                    axis=alt.Axis(format='%H:%M', grid=True, gridDash=[4, 4]),
                    sort='descending',
                ),
                tooltip=['date', 'time']
            )
        ).properties(
            title="Tweet Times",
            width=1200,
            height=800
        )
        st.altair_chart(c, use_container_width=True)

    st.markdown("""
            # Welcome

            Get a cool scatter plot of your twitter history.
            
            1. Choose your timezone
            2. Upload the `twitter-headers.js` file from your twitter backup
            3. Skeet the picture?
            4. Say hi: [Evan Anderson](https://bsky.app/profile/syndrowm.com)

            Shout out to:
            [Hank](https://bsky.app/profile/hankgreen.bsky.social/post/3lbldm2xeuc2c)
            [Tomnomnom](https://bsky.app/profile/tomnomnom.com/post/3lblghzb6qc2u)


            """)


    return


if __name__ == "__main__":
    main()
