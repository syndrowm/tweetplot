#!/usr/bin/env python
import altair as alt
import pytz
import streamlit as st

from util import load_data

st.set_page_config(
    page_title="Tweet Scatter plot",
    page_icon="🦋",
)


def main():

    with st.sidebar:
        st.markdown("[TweetPlot](https://tweetplot.streamlit.app)")
        st.markdown("---")
        timezone = st.selectbox(
            "Choose your timezone",
            pytz.all_timezones,
            index=pytz.all_timezones.index("US/Mountain"),
        )
        st.markdown("---")
        uploaded_file = st.file_uploader("Choose your tweet-headers.js file")
        st.markdown("---")
        st.sidebar.markdown(
            "Created by [Evan Anderson](https://bsky.app/profile/syndrowm.com)"
        )

    st.title("TweetPlot: Tweet addict Plot")

    if uploaded_file is not None and timezone is not None:
        try:
            df = load_data(uploaded_file.getvalue())
        except Exception as exc:
            st.error(
                f"Invalid file data. Please upload the tweets.js file. {exc}", icon="☠️"
            )
            return

        y_domain = (
            alt.DateTime(hours=0, minutes=0),
            alt.DateTime(hours=23, minutes=59),
        )

        c = (
            alt.Chart(df)
            .mark_circle()
            .mark_point(size=5, opacity=0.7)
            .encode(
                x=alt.X(
                    "localtime:T",
                    title="Year",
                    axis=alt.Axis(
                        format="%Y", tickCount="year", grid=True, gridDash=[4, 4]
                    ),
                ),  # Ordinal for discrete years
                y=alt.Y(
                    "hoursminutes(localtime):T",
                    title=f"Time of Tweet ({timezone})",
                    axis=alt.Axis(format="%H:%M", grid=True, gridDash=[4, 4]),
                    sort="descending",
                ).scale(domain=y_domain),
            )
        ).properties(title="TweetPlot", width=1200, height=800)
        st.altair_chart(c, use_container_width=True)

    st.markdown(open("README.md").read().replace("static/", "app/static/"))

    return


if __name__ == "__main__":
    main()
